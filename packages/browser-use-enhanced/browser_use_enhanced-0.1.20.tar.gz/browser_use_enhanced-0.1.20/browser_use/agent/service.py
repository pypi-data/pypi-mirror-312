from __future__ import annotations

import asyncio
import json
import logging
import os
import time
import uuid
from pathlib import Path
from typing import Any, Optional, Tuple, Type, TypeVar

from dotenv import load_dotenv
import google.generativeai as genai
from pydantic import BaseModel, ValidationError

from browser_use.agent.message_manager.service import MessageManager
from browser_use.agent.prompts import AgentMessagePrompt, SystemPrompt
from browser_use.agent.views import (
    ActionResult,
    AgentError,
    AgentHistory,
    AgentHistoryList,
    AgentOutput,
)
from browser_use.browser.views import BrowserState, BrowserStateHistory
from browser_use.controller.registry.views import ActionModel
from browser_use.controller.service import Controller
from browser_use.dom.history_tree_processor import DOMHistoryElement, HistoryTreeProcessor
from browser_use.telemetry.service import ProductTelemetry
from browser_use.telemetry.views import (
    AgentEndTelemetryEvent,
    AgentRunTelemetryEvent,
    AgentStepErrorTelemetryEvent,
)
from browser_use.utils import time_execution_async

load_dotenv()
logger = logging.getLogger(__name__)

T = TypeVar('T', bound=BaseModel)

class GeminiWrapper:
    """Wrapper class for Gemini to make it compatible with our agent architecture"""
    
    def __init__(self, model_name: str = "gemini-1.5-flash"):
        self.model = genai.GenerativeModel(model_name)
        
    async def ainvoke(self, messages: list[dict]) -> dict:
        """Async invoke method to match LangChain's interface"""
        # Convert messages to Gemini format
        gemini_messages = self._convert_to_gemini_messages(messages)
        
        # Generate response
        response = await self.model.generate_content_async(gemini_messages)
        
        return {
            "content": response.text,
            "parsed": self._parse_structured_output(response.text)
        }
    
    def _convert_to_gemini_messages(self, messages: list[dict]) -> str:
        """Convert LangChain message format to Gemini format"""
        formatted_messages = []
        for msg in messages:
            role = "system" if msg["role"] == "system" else "user"
            content = msg["content"]
            formatted_messages.append(f"{role}: {content}")
        return "\n".join(formatted_messages)
    
    def _parse_structured_output(self, text: str) -> dict:
        """Parse the structured output from Gemini's response"""
        try:
            # Extract JSON from the response
            json_start = text.find('{')
            json_end = text.rfind('}') + 1
            if json_start >= 0 and json_end > json_start:
                json_str = text[json_start:json_end]
                return json.loads(json_str)
            return {}
        except json.JSONDecodeError:
            return {}
    
    def with_structured_output(self, output_class: Type[BaseModel], include_raw: bool = True):
        """Method to support structured output similar to LangChain"""
        self.output_class = output_class
        return self

class Agent:
    def __init__(
        self,
        task: str,
        api_key: str,
        controller: Optional[Controller] = None,
        use_vision: bool = True,
        save_conversation_path: Optional[str] = None,
        max_failures: int = 5,
        retry_delay: int = 10,
        system_prompt_class: Type[SystemPrompt] = SystemPrompt,
        max_input_tokens: int = 128000,
        validate_output: bool = False,
    ):
        self.agent_id = str(uuid.uuid4())

        # Initialize Gemini
        genai.configure(api_key=api_key)
        self.llm = GeminiWrapper()
        
        self.task = task
        self.use_vision = use_vision
        self.save_conversation_path = save_conversation_path
        self._last_result = None

        # Controller setup
        self.controller_injected = controller is not None
        self.controller = controller or Controller()

        self.system_prompt_class = system_prompt_class

        # Telemetry setup
        self.telemetry = ProductTelemetry()

        # Action and output models setup
        self._setup_action_models()

        self.max_input_tokens = max_input_tokens

        self.message_manager = MessageManager(
            llm=self.llm,
            task=self.task,
            action_descriptions=self.controller.registry.get_prompt_description(),
            system_prompt_class=self.system_prompt_class,
            max_input_tokens=self.max_input_tokens,
        )

        # Tracking variables
        self.history: AgentHistoryList = AgentHistoryList(history=[])
        self.n_steps = 1
        self.consecutive_failures = 0
        self.max_failures = max_failures
        self.retry_delay = retry_delay
        self.validate_output = validate_output

        if save_conversation_path:
            logger.info(f'Saving conversation to {save_conversation_path}')

    # ... [rest of the Agent class methods remain the same] ...
    def _setup_action_models(self) -> None:
        """Setup dynamic action models from controller's registry"""
        # Get the dynamic action model from controller's registry
        self.ActionModel = self.controller.registry.create_action_model()
        # Create output model with the dynamic actions
        self.AgentOutput = AgentOutput.type_with_custom_actions(self.ActionModel)

    @time_execution_async('--step')
    async def step(self) -> None:
        """Execute one step of the task"""
        logger.info(f'\n📍 Step {self.n_steps}')
        state = None

        try:
            state = await self.controller.browser.get_state(use_vision=self.use_vision)
            self.message_manager.add_state_message(state, self._last_result)
            input_messages = self.message_manager.get_messages()
            model_output = await self.get_next_action(input_messages)
            self._save_conversation(input_messages, model_output)
            self.message_manager._remove_last_state_message()
            self.message_manager.add_model_output(model_output)

            result = await self.controller.act(model_output.action)
            self._last_result = result

            if result.extracted_content:
                logger.info(f'📄 Result: {result.extracted_content}')
            if result.is_done:
                logger.result(f'{result.extracted_content}')

            self.consecutive_failures = 0

        except Exception as e:
            result = self._handle_step_error(e)
            self._last_result = result

            if result.error:
                self.telemetry.capture(
                    AgentStepErrorTelemetryEvent(
                        agent_id=self.agent_id,
                        error=result.error,
                    )
                )
            model_output = None
        finally:
            if state:
                self._make_history_item(model_output, state, result)

    def _handle_step_error(self, error: Exception) -> ActionResult:
        """Handle all types of errors that can occur during a step"""
        error_msg = AgentError.format_error(error, include_trace=True)
        prefix = f'❌ Result failed {self.consecutive_failures + 1}/{self.max_failures} times:\n '

        if isinstance(error, (ValidationError, ValueError)):
            logger.error(f'{prefix}{error_msg}')
            if 'Max token limit reached' in error_msg:
                # cut tokens from history
                self.message_manager.max_input_tokens = self.max_input_tokens - 500
                logger.info(
                    f'Cutting tokens from history - new max input tokens: {self.message_manager.max_input_tokens}'
                )
                self.message_manager.cut_messages()
            self.consecutive_failures += 1
        elif isinstance(error, genai.types.generation_types.BlockedPromptException):
            # Handle Gemini-specific rate limiting
            logger.warning(f'{prefix}Rate limit exceeded: {error_msg}')
            time.sleep(self.retry_delay)
            self.consecutive_failures += 1
        else:
            logger.error(f'{prefix}{error_msg}')
            self.consecutive_failures += 1

        return ActionResult(error=error_msg, include_in_memory=True)

    def _make_history_item(
        self,
        model_output: AgentOutput | None,
        state: BrowserState,
        result: ActionResult,
    ) -> None:
        """Create and store history item"""
        if model_output:
            interacted_element = AgentHistory.get_interacted_element(
                model_output, state.selector_map
            )
        else:
            interacted_element = None

        state_history = BrowserStateHistory(
            url=state.url,
            title=state.title,
            tabs=state.tabs,
            interacted_element=interacted_element,
        )

        history_item = AgentHistory(model_output=model_output, result=result, state=state_history)
        self.history.history.append(history_item)

    @time_execution_async('--get_next_action')
    async def get_next_action(self, input_messages: list[dict]) -> AgentOutput:
        """Get next action from Gemini based on current state"""
        try:
            response = await self.llm.ainvoke(input_messages)
            parsed = self.AgentOutput.parse_obj(response['parsed'])
            self._log_response(parsed)
            self.n_steps += 1
            return parsed
        except Exception as e:
            logger.error(f"Error getting next action from Gemini: {str(e)}")
            raise

    def _log_response(self, response: Any) -> None:
        """Log the model's response"""
        if 'Success' in response.current_state.valuation_previous_goal:
            emoji = '👍'
        elif 'Failed' in response.current_state.valuation_previous_goal:
            emoji = '⚠️'
        else:
            emoji = '🤷'

        logger.info(f'{emoji} Evaluation: {response.current_state.valuation_previous_goal}')
        logger.info(f'🧠 Memory: {response.current_state.memory}')
        logger.info(f'🎯 Next Goal: {response.current_state.next_goal}')
        logger.info(f'🛠️ Action: {response.action.model_dump_json(exclude_unset=True)}')

    async def run(self, max_steps: int = 100) -> AgentHistoryList:
        """Execute the task with maximum number of steps"""
        try:
            logger.info(f'🚀 Starting task: {self.task}')

            self.telemetry.capture(
                AgentRunTelemetryEvent(
                    agent_id=self.agent_id,
                    task=self.task,
                )
            )

            for step in range(max_steps):
                if self._too_many_failures():
                    break

                await self.step()

                if self.history.is_done():
                    if self.validate_output:
                        if not await self._validate_output():
                            continue

                    logger.info('✅ Task completed successfully')
                    break
            else:
                logger.info('❌ Failed to complete task in maximum steps')

            return self.history

        finally:
            self.telemetry.capture(
                AgentEndTelemetryEvent(
                    agent_id=self.agent_id,
                    task=self.task,
                    success=self.history.is_done(),
                    steps=len(self.history.history),
                )
            )
            if not self.controller_injected:
                await self.controller.browser.close()

    async def _validate_output(self) -> bool:
        """Validate the output of the last action using Gemini"""
        system_msg = {
            "role": "system",
            "content": (
                f'You are a validator of an agent who interacts with a browser. '
                f'Validate if the output of last action is what the user wanted and if the task is completed. '
                f'If the task is unclear defined, you can let it pass. '
                f'Task: {self.task}. Return a JSON object with 2 keys: is_valid and reason. '
                f'is_valid is a boolean that indicates if the output is correct. '
                f'reason is a string that explains why it is valid or not.'
            )
        }

        if self.controller.browser.session:
            state = self.controller.browser.session.cached_state
            content = AgentMessagePrompt(state=state, result=self._last_result)
            msg = [system_msg, {"role": "user", "content": content.get_user_message()}]
        else:
            return True

        class ValidationResult(BaseModel):
            is_valid: bool
            reason: str

        validator = self.llm.with_structured_output(ValidationResult)
        response = await validator.ainvoke(msg)
        parsed = ValidationResult.parse_obj(response['parsed'])
        
        is_valid = parsed.is_valid
        if not is_valid:
            logger.info(f'❌ Validator decision: {parsed.reason}')
            msg = f'The output is not yet correct. {parsed.reason}.'
            self._last_result = ActionResult(extracted_content=msg, include_in_memory=True)
        else:
            logger.info(f'✅ Validator decision: {parsed.reason}')
        return is_valid

    async def rerun_history(
        self,
        history: AgentHistoryList,
        max_retries: int = 3,
        skip_failures: bool = True,
        delay_between_actions: float = 2.0,
    ) -> list[ActionResult]:
        """Rerun a saved history of actions"""
        results = []

        for i, history_item in enumerate(history.history):
            goal = (
                history_item.model_output.current_state.next_goal
                if history_item.model_output
                else ''
            )
            logger.info(f'Replaying step {i + 1}/{len(history.history)}: goal: {goal}')

            if not history_item.model_output or not history_item.model_output.action:
                logger.warning(f'Step {i + 1}: No action to replay, skipping')
                results.append(ActionResult(error='No action to replay'))
                continue

            retry_count = 0
            while retry_count < max_retries:
                try:
                    result = await self._execute_history_step(history_item, delay_between_actions)
                    results.append(result)
                    break
                except Exception as e:
                    retry_count += 1
                    if retry_count == max_retries:
                        error_msg = f'Step {i + 1} failed after {max_retries} attempts: {str(e)}'
                        logger.error(error_msg)
                        if not skip_failures:
                            results.append(ActionResult(error=error_msg))
                            raise RuntimeError(error_msg)
                    else:
                        logger.warning(
                            f'Step {i + 1} failed (attempt {retry_count}/{max_retries}), retrying...'
                        )
                        await asyncio.sleep(delay_between_actions)

        return results

    def save_history(self, file_path: Optional[str | Path] = None) -> None:
        """Save the history to a file"""
        if not file_path:
            file_path = 'AgentHistory.json'
        self.history.save_to_file(file_path)

    async def load_and_rerun(
        self, history_file: Optional[str | Path] = None, **kwargs
    ) -> list[ActionResult]:
        """Load history from file and rerun it"""
        if not history_file:
            history_file = 'AgentHistory.json'
        history = AgentHistoryList.load_from_file(history_file, self.AgentOutput)
        return await self.rerun_history(history, **kwargs)
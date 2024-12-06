from __future__ import annotations

import logging
from datetime import datetime
from typing import List, Optional, Type, Union
from google.generativeai import GenerativeModel
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_anthropic import ChatAnthropic
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import (
    AIMessage,
    BaseMessage,
    HumanMessage,
    SystemMessage,
    get_buffer_string,
)
from langchain_openai import ChatOpenAI

from browser_use.agent.message_manager.views import MessageHistory, MessageMetadata
from browser_use.agent.prompts import AgentMessagePrompt, SystemPrompt
from browser_use.agent.views import ActionResult, AgentOutput
from browser_use.browser.views import BrowserState

logger = logging.getLogger(__name__)

class MessageManager:
    def __init__(
        self,
        llm: Union[BaseChatModel, GenerativeModel],
        task: str,
        action_descriptions: str,
        system_prompt_class: Type[SystemPrompt],
        max_input_tokens: int = 128000,
        estimated_tokens_per_character: int = 3,
        image_tokens: int = 800,
    ):
        self.llm = llm
        self.system_prompt_class = system_prompt_class
        self.max_input_tokens = max_input_tokens
        self.history = MessageHistory()
        self.task = task
        self.action_descriptions = action_descriptions
        self.ESTIMATED_TOKENS_PER_CHARACTER = estimated_tokens_per_character
        self.IMG_TOKENS = image_tokens

        # Handle different model types
        if isinstance(llm, GenerativeModel):
            self.model_type = "gemini"
            # Wrap Gemini model with LangChain interface if needed
            self.llm = ChatGoogleGenerativeAI(model=llm.model_name)
        elif isinstance(llm, ChatOpenAI):
            self.model_type = "openai"
        elif isinstance(llm, ChatAnthropic):
            self.model_type = "anthropic"
        else:
            self.model_type = "unknown"

        system_message = self.system_prompt_class(
            self.action_descriptions, current_date=datetime.now()
        ).get_system_message()
        self._add_message_with_tokens(system_message)

        task_message = HumanMessage(content=f'Your task is: {task}')
        self._add_message_with_tokens(task_message)

    def _count_tokens(self, message: BaseMessage) -> int:
        """Count tokens in a message using the model's tokenizer"""
        tokens = 0
        if isinstance(message.content, list):
            for item in message.content:
                if 'image_url' in item:
                    tokens += self.IMG_TOKENS
                elif isinstance(item, dict) and 'text' in item:
                    tokens += self._count_text_tokens(item['text'])
                # Handle Gemini's image type if present
                elif isinstance(item, dict) and 'image' in item:
                    tokens += self.IMG_TOKENS
        else:
            tokens += self._count_text_tokens(message.content)
        return tokens

    def _count_text_tokens(self, text: str) -> int:
        """Count tokens in a text string based on model type"""
        try:
            if self.model_type == "gemini":
                # Use Gemini's token counting method
                return self.llm.get_num_tokens(text)
            elif self.model_type in ["openai", "anthropic"]:
                return self.llm.get_num_tokens(text)
            else:
                # Fallback to estimation
                return len(text) // self.ESTIMATED_TOKENS_PER_CHARACTER
        except Exception as e:
            logger.warning(f"Error counting tokens: {e}. Using estimation method.")
            return len(text) // self.ESTIMATED_TOKENS_PER_CHARACTER

    def add_state_message(self, state: BrowserState, result: Optional[ActionResult] = None) -> None:
        """Add browser state as human message with model-specific handling"""
        if result and result.include_in_memory:
            if result.extracted_content:
                msg = HumanMessage(content=str(result.extracted_content))
                self._add_message_with_tokens(msg)
            if result.error:
                msg = HumanMessage(content=str(result.error))
                self._add_message_with_tokens(msg)
            result = None

        # Model-specific message formatting
        if self.model_type == "gemini":
            state_message = self._format_gemini_state_message(state, result)
        else:
            state_message = AgentMessagePrompt(state, result).get_user_message()
        
        self._add_message_with_tokens(state_message)

    def _format_gemini_state_message(self, state: BrowserState, result: Optional[ActionResult]) -> HumanMessage:
        """Format state message specifically for Gemini"""
        # Gemini-specific message formatting
        # You might need to adjust this based on Gemini's specific requirements
        content = []
        
        # Add text content
        text_content = AgentMessagePrompt(state, result).get_user_message().content
        if isinstance(text_content, str):
            content.append({"text": text_content})
        
        # Add images if present in state
        if hasattr(state, 'screenshots') and state.screenshots:
            for screenshot in state.screenshots:
                content.append({
                    "image": screenshot,
                    "type": "image/png"  # Adjust based on actual image type
                })
        
        return HumanMessage(content=content)

    def cut_messages(self):
        """Get current message list, potentially trimmed to max tokens with model-specific handling"""
        diff = self.history.total_tokens - self.max_input_tokens
        if diff <= 0:
            return None

        msg = self.history.messages[-1]

        # Handle list content (including Gemini's image format)
        if isinstance(msg.message.content, list):
            text = ''
            for item in msg.message.content:
                if any(key in item for key in ['image_url', 'image']):
                    msg.message.content.remove(item)
                    diff -= self.IMG_TOKENS
                    msg.metadata.input_tokens -= self.IMG_TOKENS
                    self.history.total_tokens -= self.IMG_TOKENS
                    logger.debug(
                        f'Removed image with {self.IMG_TOKENS} tokens - total tokens now: {self.history.total_tokens}/{self.max_input_tokens}'
                    )
                elif 'text' in item and isinstance(item, dict):
                    text += item['text']
            msg.message.content = text
            self.history.messages[-1] = msg

        if diff <= 0:
            return None

        # Rest of the cutting logic remains the same
        proportion_to_remove = diff / msg.metadata.input_tokens
        if proportion_to_remove > 0.99:
            raise ValueError(
                f'Max token limit reached - history is too long - reduce the system prompt or task less tasks or remove old messages. '
                f'proportion_to_remove: {proportion_to_remove}'
            )

        content = msg.message.content
        characters_to_remove = int(len(content) * proportion_to_remove)
        content = content[:-characters_to_remove]

        self.history.remove_message(index=-1)
        msg = HumanMessage(content=content)
        self._add_message_with_tokens(msg)
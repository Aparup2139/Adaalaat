"""
HuggingFace Inference API — Custom LLM Wrapper for LlamaIndex
"""

import os
import logging
from typing import Any, Optional, Sequence
from dotenv import load_dotenv

from llama_index.core.llms.llm import LLM
from llama_index.core.llms import (
    ChatMessage,
    ChatResponse,
    CompletionResponse,
    LLMMetadata,
)
from huggingface_hub import InferenceClient

# --- Load .env from the Backend root folder ---
backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
dotenv_path = os.path.join(backend_dir, ".env")
load_dotenv(dotenv_path)
# ----------------------------------------------

logger = logging.getLogger(__name__)


class HFInferenceLLM(LLM):
    """LlamaIndex-compatible LLM that calls the HuggingFace Inference API."""

    # Use a clean name for LlamaIndex metadata (no colons)
    model_name: str = "meta-llama-Llama-3.1-8B-Instruct"
    # The actual API model identifier (may contain provider routing like :novita)
    api_model: str = "meta-llama/Llama-3.1-8B-Instruct:novita"
    hf_token: str = ""
    max_tokens: int = 1024
    temperature: float = 0.3
    _client: Optional[Any] = None

    class Config:
        arbitrary_types_allowed = True

    def __init__(self, model_name: str = None, hf_token: str = None, **kwargs):
        # Look for either HUGGINGFACE_TOKEN or HF_TOKEN from the loaded .env
        env_token = os.environ.get("HUGGINGFACE_TOKEN", "") or os.environ.get("HF_TOKEN", "")

        # The full model name with provider routing (for API calls)
        full_model = model_name or os.environ.get("LLM_MODEL", "meta-llama/Llama-3.1-8B-Instruct:novita")
        # Clean name for LlamaIndex metadata (replace invalid chars)
        clean_name = full_model.replace(":", "-").replace("/", "-")

        super().__init__(
            model_name=clean_name,
            api_model=full_model,
            hf_token=hf_token or env_token,
            **kwargs,
        )

        if not self.hf_token:
            raise ValueError("HUGGINGFACE_TOKEN or HF_TOKEN is required in your .env file for HFInferenceLLM")

        self._client = InferenceClient(api_key=self.hf_token)
        logger.info(f"HFInferenceLLM initialized: {self.api_model}")

    @property
    def metadata(self) -> LLMMetadata:
        return LLMMetadata(
            model_name=self.model_name,
            context_window=4096,
            num_output=self.max_tokens,
            is_chat_model=True,
        )

    def _convert_messages(self, messages: Sequence[ChatMessage]) -> list:
        return [
            {"role": str(msg.role).split(".")[-1], "content": msg.content}
            for msg in messages
        ]

    def chat(self, messages: Sequence[ChatMessage], **kwargs) -> ChatResponse:
        hf_messages = self._convert_messages(messages)

        try:
            completion = self._client.chat.completions.create(
                model=self.api_model,  # Use the full model name with provider
                messages=hf_messages,
                max_tokens=kwargs.get("max_tokens", self.max_tokens),
                temperature=kwargs.get("temperature", self.temperature),
            )

            content = completion.choices[0].message.content
            return ChatResponse(
                message=ChatMessage(role="assistant", content=content),
            )
        except Exception as e:
            logger.error(f"HF Inference chat failed: {e}")
            return ChatResponse(
                message=ChatMessage(
                    role="assistant",
                    content=f"I encountered an error processing your request: {str(e)}",
                ),
            )

    async def achat(self, messages: Sequence[ChatMessage], **kwargs) -> ChatResponse:
        return self.chat(messages, **kwargs)

    def complete(self, prompt: str, **kwargs) -> CompletionResponse:
        messages = [ChatMessage(role="user", content=prompt)]
        chat_resp = self.chat(messages, **kwargs)
        return CompletionResponse(text=chat_resp.message.content)

    async def acomplete(self, prompt: str, **kwargs) -> CompletionResponse:
        return self.complete(prompt, **kwargs)

    def stream_chat(self, messages, **kwargs):
        raise NotImplementedError("Streaming not implemented for HF Inference API")

    def stream_complete(self, prompt, **kwargs):
        raise NotImplementedError("Streaming not implemented for HF Inference API")

    async def astream_chat(self, messages, **kwargs):
        raise NotImplementedError("Async streaming not implemented for HF Inference API")

    async def astream_complete(self, prompt, **kwargs):
        raise NotImplementedError("Async streaming not implemented for HF Inference API")
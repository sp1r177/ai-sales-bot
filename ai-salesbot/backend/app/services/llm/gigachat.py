from __future__ import annotations

import asyncio
from typing import Any, Dict, List

import httpx

from .base import LLMProvider, MessageDict
from ...core.config import get_settings


class GigaChatProvider(LLMProvider):
    def generate(self, messages: List[MessageDict], temperature: float = 0.7, max_tokens: int = 512) -> str:
        return asyncio.run(self._generate_async(messages, temperature, max_tokens))

    async def _generate_async(self, messages: List[MessageDict], temperature: float, max_tokens: int) -> str:
        settings = get_settings()
        if not settings.LLM_API_URL:
            raise RuntimeError("LLM_API_URL is not set. Please set it according to the official GigaChat docs.")
        headers = {
            "Authorization": f"Bearer {settings.LLM_API_KEY}" if settings.LLM_API_KEY else "",
            "Content-Type": "application/json",
        }
        payload = {
            "model": settings.LLM_MODEL,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }
        async with httpx.AsyncClient(timeout=settings.LLM_TIMEOUT_SECONDS) as client:
            resp = await client.post(settings.LLM_API_URL, json=payload, headers=headers)
            resp.raise_for_status()
            data = resp.json()
            # Try to extract text conservatively
            text = self._extract_text(data)
            if not text:
                raise RuntimeError("Empty response")
            return text

    def _extract_text(self, data: Dict[str, Any]) -> str | None:
        # common patterns: choices[0].message.content or choices[0].text or data["text"]
        try:
            choices = data.get("choices") or []
            if choices:
                choice = choices[0]
                if isinstance(choice, dict):
                    msg = choice.get("message")
                    if isinstance(msg, dict) and isinstance(msg.get("content"), str):
                        return msg["content"]
                    if isinstance(choice.get("text"), str):
                        return choice["text"]
        except Exception:
            pass
        # flat text fields
        for key in ("content", "text"):
            val = data.get(key)
            if isinstance(val, str) and val.strip():
                return val
        return None
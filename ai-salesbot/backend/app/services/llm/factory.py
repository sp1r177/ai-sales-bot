from __future__ import annotations

from .base import LLMProvider
from .gigachat import GigaChatProvider
from .yandexgpt import YandexGPTProvider
from ...core.config import get_settings


def get_llm_provider() -> LLMProvider:
    settings = get_settings()
    provider = (settings.LLM_PROVIDER or "").lower()
    if provider == "yandexgpt":
        return YandexGPTProvider()
    # default
    return GigaChatProvider()
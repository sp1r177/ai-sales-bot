import json
import types

import httpx
import pytest

from backend.app.services.llm.gigachat import GigaChatProvider
from backend.app.services.llm.yandexgpt import YandexGPTProvider
from backend.app.core.config import get_settings


class DummyResponse:
    def __init__(self, json_data, status_code=200):
        self._json = json_data
        self.status_code = status_code

    def raise_for_status(self):
        if not (200 <= self.status_code < 300):
            raise httpx.HTTPStatusError("", request=None, response=None)

    def json(self):
        return self._json


@pytest.fixture(autouse=True)
def set_llm_env(monkeypatch):
    s = get_settings()
    monkeypatch.setenv("LLM_API_URL", "http://example.org/mock")
    monkeypatch.setenv("LLM_API_KEY", "test")
    return s


@pytest.mark.parametrize("provider_cls", [GigaChatProvider, YandexGPTProvider])
def test_provider_extracts_text(monkeypatch, provider_cls):
    async def mock_post(self, url, json=None, headers=None):
        return DummyResponse({"choices": [{"message": {"content": "hello"}}]})

    monkeypatch.setattr(httpx.AsyncClient, "post", mock_post)

    provider = provider_cls()
    text = provider.generate([{"role": "user", "content": "hi"}])
    assert text == "hello"
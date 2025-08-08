from __future__ import annotations

import abc
from typing import Any, Dict, List


MessageDict = Dict[str, Any]


class LLMProvider(abc.ABC):
    @abc.abstractmethod
    def generate(self, messages: List[MessageDict], temperature: float = 0.7, max_tokens: int = 512) -> str:  # noqa: D401
        """Generate completion text for chat messages. Must be sync. Implementations may use Async under the hood."""
        raise NotImplementedError
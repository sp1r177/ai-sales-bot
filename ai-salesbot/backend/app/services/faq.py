from __future__ import annotations

from typing import List


def format_faq_bullets(items: List[str]) -> str:
    if not items:
        return ""
    return "\n".join(f"- {item}" for item in items)
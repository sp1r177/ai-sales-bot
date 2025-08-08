from backend.app.api.v1.dialogs import _build_messages
from backend.app.models.bot import Bot


def test_build_messages_contains_rules():
    bot = Bot(
        id=1,
        owner_id=1,
        name="Товар",
        description="Описание",
        characteristics={"цвет": "красный"},
        images=[],
        price=1000.0,
        discount_percent=15.0,
        wholesale_price=800.0,
        pay_url=None,
        pay_url_discount=None,
        bargaining_style="standard",
        faq=["Есть доставка?", "Гарантия?"],
        model_preset=None,
    )
    msgs = _build_messages(bot, "Привет")
    assert any("никогда" in m["content"].lower() for m in msgs if m["role"] == "system")
    assert any(m["role"] == "assistant" for m in msgs)
    assert msgs[-1]["role"] == "user"
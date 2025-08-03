import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from customer import Customer, Rate
from utils import replace_or_add_rate


def test_add_rate_increases_rate_count():
    customer = Customer("Test Co")
    rate = Rate("MEL", "SHA", "20GP", 800, 400, 200, 300, 35, 30, "COLLECT", "14 Days")

    assert len(customer.rates) == 0
    customer.add_rate(rate)
    assert len(customer.rates) == 1


def test_replace_or_add_rate_updates_existing_when_confirmed():
    customer = Customer("Test Co")
    original = Rate(
        "SYD", "TOKYO", "20GP", 800, 400, 200, 300, 35, 30, "COLLECT", "14 Days"
    )
    updated = Rate(
        "SYD", "TOKYO", "20GP", 900, 500, 250, 350, 40, 35, "COLLECT", "10 Days"
    )

    customer.add_rate(original)

    assert len(customer.rates) == 1
    assert customer.rates[0].freight_usd == 800

    replace_or_add_rate(customer, updated, replace_existing=True)

    assert len(customer.rates) == 1
    assert customer.rates[0].freight_usd == 900
    assert customer.rates[0].dthc == "COLLECT"


def test_replace_or_add_rate_skips_update_when_declined(monkeypatch):
    customer = Customer("Test Co")
    original = Rate(
        "SYD", "TOKYO", "20GP", 800, 400, 200, 300, 35, 30, "COLLECT", "14 Days"
    )
    updated = Rate(
        "SYD", "TOKYO", "20GP", 999, 999, 999, 999, 99, 99, "PREPAID", "99 Days"
    )

    customer.add_rate(original)

    monkeypatch.setattr(
        "questionary.confirm",
        lambda prompt: type("FakePrompt", (), {"ask": staticmethod(lambda: False)}),
    )

    replace_or_add_rate(customer, updated, replace_existing=None)

    assert len(customer.rates) == 1
    assert customer.rates[0].freight_usd == 800
    assert customer.rates[0].dthc == "COLLECT"

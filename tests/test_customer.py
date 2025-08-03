import sys
import os
import glob

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils import replace_or_add_rate, export_rates_to_excel
from main import import_quote
from customer import Customer, Rate


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


def test_replace_or_add_rate_adds_new_rate_when_no_existing_rate():
    customer = Customer("Test Co")
    original = Rate(
        "SYD", "TOKYO", "20GP", 800, 400, 200, 300, 35, 30, "COLLECT", "14 Days"
    )
    new_rate = Rate(
        "MEL", "BUSAN", "40HC", 999, 999, 999, 999, 99, 99, "PREPAID", "21 Days"
    )

    customer.add_rate(original)

    replace_or_add_rate(customer, new_rate, replace_existing=None)

    assert len(customer.rates) == 2
    assert any(
        r.load_port == "MEL"
        and r.destination_port == "BUSAN"
        and r.container_type == "40HC"
        for r in customer.rates
    )


def test_replace_or_add_rate_skips_update_when_prompt_return_none(monkeypatch):
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
        lambda prompt: type("FakePrompt", (), {"ask": staticmethod(lambda: None)}),
    )

    replace_or_add_rate(customer, updated, replace_existing=None)

    assert len(customer.rates) == 1
    assert customer.rates[0].freight_usd == 800
    assert customer.rates[0].dthc == "COLLECT"


def test_export_rates_to_excel(tmp_path):
    customer = Customer("Test Co")
    customer.add_rate(
        Rate("SYD", "TOKYO", "20GP", 999, 999, 999, 999, 99, 99, "PREPAID", "99 Days")
    )

    export_dir = tmp_path / "exports"
    file_prefix = "test_export"

    export_rates_to_excel(customer.rates, file_prefix, directory=str(export_dir))

    matches = list(glob.glob(f"{export_dir}/{file_prefix}_*.xlsx"))
    assert matches, "Expected Excel export file was not created"


def test_import_quote_adds_rate(tmp_path, monkeypatch):
    customer = Customer("Test Co")
    customer.add_rate(
        Rate("SYD", "TOKYO", "20GP", 500, 300, 100, 200, 40, 20, "COLLECT", "14 Days")
    )

    file_prefix = "test_import"
    export_rates_to_excel(customer.rates, file_prefix, directory=str(tmp_path))
    matches = list(glob.glob(f"{tmp_path}/{file_prefix}_*.xlsx"))
    assert matches, "Test export file not found"
    file_path = matches[0]

    monkeypatch.setattr("main.load_data", lambda: [customer])

    monkeypatch.setattr(
        "questionary.text",
        lambda *args, **kwargs: type(
            "Prompt", (), {"ask": staticmethod(lambda: str(file_path))}
        )(),
    )
    monkeypatch.setattr(
        "questionary.select",
        lambda *args, **kwargs: type(
            "Prompt", (), {"ask": staticmethod(lambda: "Test Co")}
        )(),
    )
    monkeypatch.setattr(
        "questionary.confirm",
        lambda *args, **kwargs: type(
            "Prompt", (), {"ask": staticmethod(lambda: True)}
        )(),
    )

    customer.rates = []
    import_quote()

    assert len(customer.rates) == 1
    assert customer.rates[0].load_port == "SYD"

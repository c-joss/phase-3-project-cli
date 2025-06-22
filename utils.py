import json
import questionary
from customer import Customer, Rate, TariffRate, Manager
from openpyxl import Workbook
from openpyxl.styles import Font
from datetime import datetime
import re
import os

DATA_FILE = "data/rates.json"
TARIFF_FILE = "data/tariff.json"
EXPORT_DIR = "exports"

VALID_LOAD_PORTS = ["Melbourne", "Sydney", "Brisbane", "AU"]
VALID_DEST_PORTS = [
    "Shanghai",
    "Ningbo",
    "Shekou",
    "Xingang",
    "Qingdao",
    "Zhangjiagang",
    "Kaohsiung",
    "Taichung",
    "Keelung",
]
VALID_CONTAINERS = ["20GP", "40GP", "40HC", "20RE", "40REHC", "20OT", "40OT"]
VALID_DTHC = ["Collect", "Prepaid"]


def load_data():
    try:
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
            customers = []
            for c in data:
                customer = Customer(c["name"])
                for r in c["rates"]:
                    rate = Rate(
                        r["load_port"],
                        r["destination_port"],
                        r.get("container_type", ""),
                        r["freight_usd"],
                        r["othc_aud"],
                        r["doc_aud"],
                        r["cmr_aud"],
                        r["ams_usd"],
                        r["lss_usd"],
                        r["dthc"],
                        r["free_time"],
                    )
                    customer.add_rate(rate)
                customers.append(customer)
            return customers
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_data(customers):
    with open(DATA_FILE, "w") as f:
        json.dump([c.to_dict() for c in customers], f, indent=4)


def load_tariff():
    try:
        with open(TARIFF_FILE, "r") as f:
            data = json.load(f)
            tariffs = []
            for r in data:
                rate = TariffRate(
                    r["load_port"],
                    r["destination_port"],
                    r["container_type"],
                    {
                        "freight_usd": r["freight_usd"],
                        "othc_aud": r["othc_aud"],
                        "doc_aud": r["doc_aud"],
                        "cmr_aud": r["cmr_aud"],
                        "ams_usd": r["ams_usd"],
                        "lss_usd": r["lss_usd"],
                        "dthc": r["dthc"],
                        "free_time": r["free_time"],
                    },
                )
                tariffs.append(rate)
            return tariffs
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_tariff(tariffs):
    with open(TARIFF_FILE, "w") as f:
        json.dump([rate.to_dict() for rate in tariffs], f, indent=4)


def format_rate_choice(rate, index):
    return f"{index + 1}: {rate.load_port} to {rate.destination_port} ({rate.container_type})"


class TariffManager(Manager):
    def __init__(self):
        super().__init__()
        self.load_tariffs()

    def load_tariffs(self):
        self.items = load_tariff()

    def save_tariffs(self):
        save_tariff(self.items)

    def add_tariffs(self, load_port, destination_port, container_type, values):
        rate = TariffRate(load_port, destination_port, container_type, values)
        self.add(rate)
        self.save_tariffs()

    def view_tariffs(self):
        if not self.items:
            print("\n No Tariff rate found.")
            return

        for r in self.items:
            print(str(r))

    def delete_tariff(self):
        if not self.items:
            print("\n No Tariff rates to delete.")
            return
        choices = [format_rate_choice(r, idx) for idx, r in enumerate(self.items)]
        selected = questionary.select("Select Tariff to delete:", choices=choices).ask()
        rate_idx = int(selected.split(":")[0]) - 1
        confirm = questionary.confirm("Confirm to delete tariff?").ask()
        if confirm:
            deleted = self.items.pop(rate_idx)
            self.save_tariffs()
            print(
                f"\n Deleted tariffs: {deleted.load_port} to {deleted.destination_port} ({deleted.container_type})\n"
            )
        else:
            print("\nCancelled.\n")

    def export_tariff_rates(self):
        export_rates_to_excel(self.items, filename_prefix="Tariff_Rates")


def export_rates_to_excel(rates, filename_prefix):

    if not rates:
        print("\n No rates found.")
        return

    wb = Workbook()
    ws = wb.active
    ws.title = "Rates"

    ws["A1"] = f"{filename_prefix} Export"
    ws["A1"].font = Font(bold=True, size=14)

    ws.append([])

    headers = [
        "POL",
        "POD",
        "Container",
        "Freight USD",
        "OTHC AUD",
        "DOC AUD",
        "CMR AUD",
        "AMS USD",
        "LSS USD",
        "DTHC",
        "Free Time",
    ]
    ws.append(headers)

    for cell in ws[3]:
        cell.font = Font(bold=True)

    for rate in rates:
        row = [
            getattr(rate, "load_port", ""),
            getattr(rate, "destination_port", ""),
            getattr(rate, "container_type", ""),
            getattr(rate, "freight_usd", ""),
            getattr(rate, "othc_aud", ""),
            getattr(rate, "doc_aud", ""),
            getattr(rate, "cmr_aud", ""),
            getattr(rate, "ams_usd", ""),
            getattr(rate, "lss_usd", ""),
            getattr(rate, "dthc", ""),
            getattr(rate, "free_time", ""),
        ]
        ws.append(row)

    for column_cells in ws.columns:
        length = max(len(str(cell.value)) for cell in column_cells)
        col_letter = column_cells[0].column_letter
        ws.column_dimensions[col_letter].width = length + 2

    current_date = datetime.now().strftime("%d_%m_%Y")
    filename = f"{EXPORT_DIR}/{filename_prefix}_{current_date}.xlsx"
    wb.save(filename)

    print(f"\n Exported to {len(rates)} rates to {filename}\n")


def rate_values_prompt(defaults=None):
    defaults = defaults or {}

    load_port = questionary.autocomplete(
        "Enter Load Port:",
        choices=VALID_LOAD_PORTS,
        default=defaults.get("load_port", ""),
        validate=lambda text: text in VALID_LOAD_PORTS or "Please select a valid port",
    ).ask()

    destination_port = questionary.autocomplete(
        "Enter Destination Port:",
        choices=VALID_DEST_PORTS,
        default=defaults.get("destination_port", ""),
        validate=lambda text: text in VALID_DEST_PORTS or "Please select a valid port",
    ).ask()

    container_type_default = defaults.get("container_type", "")
    container_type = questionary.select(
        "Select Container Type:",
        choices=VALID_CONTAINERS,
        default=(
            container_type_default
            if container_type_default in VALID_CONTAINERS
            else None
        ),
    ).ask()

    freight_usd = questionary.text(
        "Freight (USD):", default=defaults.get("freight_usd", "")
    ).ask()
    othc_aud = questionary.text(
        "OTHC (AUD):", default=defaults.get("othc_aud", "")
    ).ask()
    doc_aud = questionary.text("DOC (AUD):", default=defaults.get("doc_aud", "")).ask()
    cmr_aud = questionary.text("CMR (AUD):", default=defaults.get("cmr_aud", "")).ask()
    ams_usd = questionary.text("AMS (USD):", default=defaults.get("ams_usd", "")).ask()
    lss_usd = questionary.text("LSS (USD):", default=defaults.get("lss_usd", "")).ask()
    dthc_default = defaults.get("dthc", "")
    dthc = questionary.select(
        "Select DTHC Terms:",
        choices=VALID_DTHC,
        default=dthc_default if dthc_default in VALID_DTHC else None,
    ).ask()
    free_time = questionary.text(
        "Free Time:", default=defaults.get("free_time", "")
    ).ask()

    return {
        "load_port": load_port,
        "destination_port": destination_port,
        "container_type": container_type,
        "freight_usd": freight_usd,
        "othc_aud": othc_aud,
        "doc_aud": doc_aud,
        "cmr_aud": cmr_aud,
        "ams_usd": ams_usd,
        "lss_usd": lss_usd,
        "dthc": dthc,
        "free_time": free_time,
    }

import json
import questionary
from customer import Customer, Rate, TariffRate
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


class TariffManager:
    def __init__(self):
        self.tariffs = self.load_tariff()

    def save_tariff(self):
        with open(TARIFF_FILE, "w") as f:
            json.dump([rate.to_dict() for rate in self.tariffs], f)

    def load_tariff(self):
        try:
            with open(TARIFF_FILE, "r") as f:
                data = json.load(f)
                return [
                    TariffRate(
                        r["load_port"],
                        r["destination_port"],
                        r["container_type"],
                        r,
                    )
                    for r in data
                ]
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def add_tariff(self, load_port, destination_port, container_type, values):
        rate = TariffRate(load_port, destination_port, container_type, values)
        self.tariffs.append(rate)
        self.save_tariff()

    def view_tariffs(self):
        if not self.tariffs:
            print("\n No Tariff rate found.")
            return
        for r in self.tariffs:
            print(
                f"{r.load_port} to {r.destination_port} ({r.container_type}) | "
                f"Freight: {r.freight_usd} USD | OTHC: {r.othc_aud} AUD | "
                f"DOC: {r.doc_aud} AUD | CMR: {r.cmr_aud} AUD | AMS: {r.ams_usd} USD | "
                f"LSS: {r.lss_usd} USD | DTHC: {r.dthc} | Free Time: {r.free_time}"
            )

    def delete_tariff(self):
        if not self.tariffs:
            print("\n No Tariff rates to delete.")
            return
        choices = [
            f"{idx + 1}: {r.load_port} to {r.destination_port} ({r.container_type})"
            for idx, r in enumerate(self.tariffs)
        ]
        selected = questionary.select("Select Tariff to delete:", choices=choices).ask()
        rate_idx = int(selected.split(":")[0]) - 1
        confirm = questionary.confirm("Confirm to delete tariff?").ask()
        if confirm:
            deleted = self.tariffs.pop(rate_idx)
            self.save_tariff()
            print(
                f"\n Deleted tariffs: {deleted.load_port} to {deleted.destination_port}\n"
            )
        else:
            print("\nCancelled.\n")

    def export_tariff_rates(self):
        export_rates_to_excel(self.tariffs, filename_prefix="Tariff_Rates")


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

import json
import questionary
from customer import Customer, Rate, TariffRate

DATA_FILE = "data/rates.json"
TARIFF_FILE = "data/tariff.json"

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

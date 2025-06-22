import json
from customer import Customer, Rate

DATA_FILE = "data/rates.json"

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

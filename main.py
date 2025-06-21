import questionary
from customer import Rate, Customer
from tabulate import tabulate
from utils import (
    load_data,
    save_data,
    VALID_LOAD_PORTS,
    VALID_DEST_PORTS,
    VALID_CONTAINERS,
)


def main_menu():
    while True:
        choice = questionary.select(
            "What would you like to do?",
            choices=[
                "Add Rate",
                "View Rates",
                "Edit Rates",
                "Delete Rate",
                "Export Quote",
                "Exit",
            ],
        ).ask()

        if choice == "Add Rate":
            add_rate()
        elif choice == "View Rates":
            view_rates()
        elif choice == "Edit Rates":
            edit_rates()
        elif choice == "Delete Rate":
            delete_rate()
        elif choice == "Export Quote":
            export_quote()
        elif choice == "Exit":
            print("Exiting Rate Management App")
            break


def add_rate():
    customers = load_data()

    customer_name = questionary.text("Enter customer name:").ask()

    existing_customer = next((c for c in customers if c.name == customer_name), None)
    if not existing_customer:
        existing_customer = Customer(customer_name)
        customers.append(existing_customer)

    load_port = questionary.autocomplete(
        "Enter Load Port:",
        choices=VALID_LOAD_PORTS,
        validate=lambda text: text in VALID_LOAD_PORTS or "Please select a valid port",
    ).ask()
    destination_port = questionary.autocomplete(
        "Enter Destination Port:",
        choices=VALID_DEST_PORTS,
        validate=lambda text: text in VALID_DEST_PORTS or "Please select a valid port",
    ).ask()
    container_type = questionary.select(
        "Select Container Type:", choices=VALID_CONTAINERS
    ).ask()
    freight_usd = questionary.text("Freight (USD):").ask()
    othc_aud = questionary.text("OTHC (AUD):").ask()
    doc_aud = questionary.text("DOC (AUD):").ask()
    cmr_aud = questionary.text("CMR (AUD):").ask()
    ams_usd = questionary.text("AMS (USD):").ask()
    lss_usd = questionary.text("LSS (USD):").ask()
    dthc = questionary.text("DTHC:").ask()
    free_time = questionary.text("Free Time:").ask()

    rate = Rate(
        load_port,
        destination_port,
        container_type,
        freight_usd,
        othc_aud,
        doc_aud,
        cmr_aud,
        ams_usd,
        lss_usd,
        dthc,
        free_time,
    )

    existing_customer.add_rate(rate)

    save_data(customers)

    print("\n Rate added.\n")


def view_rates():
    customers = load_data()

    if not customers:
        print("\n No rates found. Please add rates first")
        return

    for customer in customers:
        print(f"\nCustomer: {customer.name}")

        table_data = []
        for rate in customer.rates:
            table_data.append(
                [
                    rate.load_port,
                    rate.destination_port,
                    rate.container_type,
                    rate.freight_usd,
                    rate.othc_aud,
                    rate.doc_aud,
                    rate.cmr_aud,
                    rate.ams_usd,
                    rate.lss_usd,
                    rate.dthc,
                    rate.free_time,
                ]
            )

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

        print(tabulate(table_data, headers=headers, tablefmt="grid"))


def edit_rates():
    customers = load_data()

    if not customers:
        print("\n No rates found.")
        return

    customer_choices = [c.name for c in customers]
    customer_name = questionary.autocomplete(
        "Select Customer:",
        choices=customer_choices,
        validate=lambda text: text in customer_choices
        or "Please select a valid customer",
    ).ask()

    customer = next(c for c in customers if c.name == customer_name)

    if not customer.rates:
        print("\n Customer has no rates.")
        return

    rate_choices = [
        f"{idx + 1}: {r.load_port} to {r.destination_port} ({r.container_type})"
        for idx, r in enumerate(customer.rates)
    ]
    selected = questionary.select("Select Rate to Edit:", choices=rate_choices).ask()
    rate_idx = int(selected.split(":")[0]) - 1
    rate = customer.rates[rate_idx]

    rate.freight_usd = questionary.text(
        "Freight (USD):", default=str(rate.freight_usd)
    ).ask()
    rate.othc_aud = questionary.text("OTHC (AUD):", default=str(rate.othc_aud)).ask()
    rate.doc_aud = questionary.text("DOC (AUD):", default=str(rate.doc_aud)).ask()
    rate.cmr_aud = questionary.text("CMR (AUD):", default=str(rate.cmr_aud)).ask()
    rate.ams_usd = questionary.text("AMS (USD):", default=str(rate.ams_usd)).ask()
    rate.lss_usd = questionary.text("LSS (USD):", default=str(rate.lss_usd)).ask()
    rate.dthc = questionary.text("DTHC:", default=str(rate.dthc)).ask()
    rate.free_time = questionary.text("Free Time:", default=str(rate.free_time)).ask()

    save_data(customers)

    print("\n Rate updated.\n")


def delete_rate():
    print("Delete rate selected")


def export_quote():
    print("Export quote selected")


if __name__ == "__main__":
    main_menu()

import questionary
from customer import Rate, Customer
from tabulate import tabulate
from openpyxl import Workbook, load_workbook
from openpyxl.styles import Font
from datetime import datetime
import re
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
                "Export Quote to Excel",
                "Import Quote from Excel",
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
        elif choice == "Export Quote to Excel":
            export_quote()
        elif choice == "Import Quote from Excel":
            import_quote()
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
    customers = load_data()

    if not customers:
        print("\n No rates found.")
        return

    customer_choices = [c.name for c in customers]
    customer_name = questionary.select(
        "Select Customer:", choices=customer_choices
    ).ask()

    customer = next(c for c in customers if c.name == customer_name)

    if not customer.rates:
        print("\n Customer has no rates.")
        return
    rate_choices = [
        f"{idx + 1}: {r.load_port} to {r.destination_port} ({r.container_type})"
        for idx, r in enumerate(customer.rates)
    ]
    selected = questionary.select("Select Rate to Delete:", choices=rate_choices).ask()

    rate_idx = int(selected.split(":")[0]) - 1

    confirm = questionary.confirm("Confirm to delete customer?").ask()

    if confirm:
        deleted = customer.rates.pop(rate_idx)
        save_data(customers)
        print(f"\n Deleted rate: {deleted.load_port} to {deleted.destination_port}\n")
    else:
        print("\nCancelled. \n")


def export_quote():
    EXPORT_DIR = "exports"
    customers = load_data()

    if not customers:
        print("\n No rates found.")
        return

    customer_choices = [c.name for c in customers]
    customer_name = questionary.select(
        "Select Customer:", choices=customer_choices
    ).ask()

    customer = next(c for c in customers if c.name == customer_name)

    if not customer.rates:
        print("\n Customer has no rates.")
        return

    wb = Workbook()
    ws = wb.active
    ws.title = "Quote"

    ws["A1"] = f"Customer: {customer.name}"
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

    for rate in customer.rates:
        row = [
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
        ws.append(row)

    for column_cells in ws.columns:
        length = max(len(str(cell.value)) for cell in column_cells)
        col_letter = column_cells[0].column_letter
        ws.column_dimensions[col_letter].width = length + 2

    safe_name = re.sub(r"\W+", "_", customer_name)
    current_date = datetime.now().strftime("%d_%m_%Y")
    filename = f"{EXPORT_DIR}/Quote_{safe_name}_{current_date}.xlsx"
    wb.save(filename)

    print(f"\n Quote exported to {filename}\n")


def import_quote():
    EXPORT_DIR = "exports"
    customers = load_data()
    file_path = questionary.text(
        "Enter path to Excel file to import., default=f{EXPORT_DIR}/"
    ).ask()

    try:
        wb = load_workbook(filename=file_path)
    except Exception as e:
        print(f"\n Could not open file: {e}\n")
        return

    ws = wb.active

    customer_choices = [c.name for c in customers]
    customer_name = questionary.select(
        "Select Customer to import rates to", choices=customer_choices
    ).ask()

    customer = next(c for c in customers if c.name == customer_name)

    for row in ws.iter_rows(min_row=4, values_only=True):
        (
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
        ) = row

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

        customer.add_rate(rate)

    save_data(customers)


if __name__ == "__main__":
    main_menu()

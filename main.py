import questionary
from customer import Rate, Customer
from utils import load_data, save_data


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

    load_port = questionary.text("Enter Load Port:").ask()
    destination_port = questionary.text("Enter Destination Port:").ask()
    container_type = questionary.text("Enter Container Type:").ask()
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


def view_rates():
    print("View rates selected")


def edit_rates():
    print("Edit rates selected")


def delete_rate():
    print("Delete rate selected")


def export_quote():
    print("Export quote selected")


if __name__ == "__main__":
    main_menu()

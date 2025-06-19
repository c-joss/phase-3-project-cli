import questionary
from customer import Rate
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
    print("Add rate selected")


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

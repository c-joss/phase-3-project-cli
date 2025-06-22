# Rate Manager App

This is a terminal based Rate Manager application for managing customer rates and tariff rates for a shipping line agency.

## Features

- Add, view, edit and delete customer rates
- Add, view, edit and delete tariff rates
- Export rates to Excel
- Import rates from Excel
- Dynamic management of valid ports
- Duplicate rate checking when importing tariff rates

## Built With

- Python
- Questionary (MIT License) - for interactive CLI menus
- OpenPyXl (MIT License) - for reading/writing Excel files
- Tabulate (MIT License) - for formatted display of rates in the console

All dependencies use permissive open-source licences. No known ethical concerns are associated with the use of these packages.

## How to Run

1. Install Python 3.
2. Clone or download this repository.
3. Create a virtual environment (recommended):

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # or venv\Scripts\activate on Windows
    ```

4. Install dependencies:

    ```bash
    pip install questionary openpyxl tabulate
    ```

5. Run the app:

    ```bash
    python3 main.py
    ```

---

## Folders

- data: where the data is stored
- exports: where Excel files are exported
- main.py: the main program

---

## Notes

- On **Import Tariff Rates**, the app will:
  - Check if a rate for a `(load port, destination port, container type)` already exists.
  - If so, and the rates are identical — skip.
  - If rates differ — prompt to update.
  - If load/destination port is new — prompt to add to valid list.
  
- On **Export Rates**, filenames include the current date for versioning.

---

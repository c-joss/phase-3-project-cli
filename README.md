# Rate Manager App

This is a terminal based Rate Manager application for managing customer rates and tariff rates for a shipping line agency.

## Features

- Add, view, edit and delete customer rates
- Add, view, edit and delete tariff rates
- Export rates to Excel (with timestamps for version control)
- Import rates from Excel (with smart duplicate and update checks)
- Dynamic management of valid ports (prompts to add unknown ports)
- Duplicate rate detection and optional replacement on import
- Input validation for key data fields (freight, surcharges, port codes)
- Clearly formatted CLI table outputs using tabulate
- Testing coverage includes core logic: rate updates, skipping, importing/exporting

## System Requirements

- Python 3.10 or higher
- Operating System: Linux, macOS, or Windows
- Recommended Terminal Size: 100x30 (for best formatting display)
- Required packages: questionary, openpyxl, tabulate, sqlalchemy, alembic, prompt-toolkit==3.0.51 
- For testing: pytest

## How to Run

1. Clone or download this repository.
2. Install dependencies with Pipenv:

    ```bash
    pipenv install
    ```

3. Activate the virtual environment:

    ```bash
    pipenv shell
    ```

4. Run the database migrations:

    ```bash
    alembic -c lib/db/alembic.ini upgrade head
    ```

5. Seed the database with initial data:

    ```bash
    python -m lib.db.seed
    ```

6. Start the CLI:

    ```bash
    python -m lib.cli
    ```

---

## Folder Structure

- `lib/cli.py` — main CLI entrypoint  
- `lib/helpers.py` — UI prompts & Excel import/export  
- `lib/db/models.py` — SQLAlchemy models  
- `lib/db/seed.py` — seed DB from JSON once  
- `lib/db/migrations/` — Alembic migrations  
- `exports/` — Excel exports  
- `tests/` — pytest tests  
- `shipping.db` — SQLite database (generated)
- `tests/conftest.py` — legacy import aliases for pytest compatibility
- `data/` — initial JSON files (rates.json, tariff.json, etc.)

---

## Testing

Unit tests are included in tests/test_customer.py, using pytest.

Coverage includes:

- Adding and replacing rates
- Exporting and importing quotes from Excel
- Skipping identical rate entries
- Handling confirmation prompts via monkeypatching

Run tests with:

```bash
pipenv run pytest
```

Note: tests use `tests/conftest.py` to alias legacy imports (`helpers`, `cli`, `main`) to the new modules. Tests also assume the database is migrated and seeded before running.

---

## Data Handling & Security

- All customer and tariff data is stored in a local SQLite database (shipping.db).
- seed.py can import initial JSON files once, but after that the DB is the source of truth.
- Sensitive data is not stored; no user credentials or personal information are collected.
- Import/export operations read and write to .xlsx files using openpyxl.
- Inputs are validated where possible to avoid malformed entries or corrupted data files.
- JSON files are stored locally and should be backed up or version controlled if needed.
- Limitation: There is no authentication or role-based access. All access assumes trusted local users.

---

## Limitations

- No GUI or web interface; CLI-only.
- Data is not encrypted or secured beyond local storage.
- Importing Excel files assumes a valid Excel format as exported by this app (e.g., headers starting at row 3).
- Duplicate rates require user confirmation to update—no batch logic or logging yet.
- No undo or rollback features.
- No user authentication; assumes trusted local usage.
- Data persists in shipping.db; back up manually if needed.

---

## Built With

- Python
- Questionary (MIT License) — interactive CLI prompts
- OpenPyXL (MIT License) — Excel file reading/writing
- Tabulate (MIT License) — console table formatting
- Pytest (MIT License) — unit testing framework

All dependencies use permissive open-source licences with no known ethical concerns.

---

## Notes

- On **Import Tariff Rates**, the app will:
  - Check if a rate for a `(load port, destination port, container type)` already exists.
  - If so, and the rates are identical — skip.
  - If rates differ — prompt to update.
  - If load/destination port is new — prompt to add to valid list.
  
- On **Export Rates**, filenames include the current date for versioning.

---

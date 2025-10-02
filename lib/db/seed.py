import json
from pathlib import Path
from lib.db.models import Base, engine, Session, Customer, Rate, Tariff

DATA_DIR = Path(__file__).resolve().parents[3] / "data"
RATES_JSON = DATA_DIR / "rates.json"
TARIFF_JSON = DATA_DIR/ "tariff.json"

def _to_float(v):
    try:
        return float(v)
    except Exception:
        return 0.0
    
def seed_customers_and_rates(session: Session):
    if not RATES_JSON.exists():
        return
    data = json.loads(RATES_JSON.read_text())
import json
from pathlib import Path
from sqlalchemy.orm import Session as OrmSession
from lib.db.models import Base, engine, Session, Customer, Rate, Tariff

DATA_DIR = Path(__file__).resolve().parents[2] / "data"
RATES_JSON = DATA_DIR / "rates.json"
TARIFF_JSON = DATA_DIR/ "tariff.json"

def _to_float(v):
    try:
        return float(v)
    except Exception:
        return 0.0

def seed_customers_and_rates(session: OrmSession):
    if not RATES_JSON.exists():
        return

    data = json.loads(RATES_JSON.read_text())

    for c in data:
        name = str(c.get("name", "")).upper().strip()
        customer = session.query(Customer).filter_by(name=name).first()
        if not customer:
            customer = Customer(name=name)
            session.add(customer)
            session.flush()

        for r in c.get("rates", []):
            rate = session.query(Rate).filter_by(
                customer_id=customer.id,
                load_port=r["load_port"],
                destination_port=r["destination_port"],
                container_type=r.get("container_type", ""),
            ).first()

            fields = dict(
                load_port=r["load_port"],
                destination_port=r["destination_port"],
                container_type=r.get("container_type", ""),
                freight_usd=_to_float(r["freight_usd"]),
                othc_aud=_to_float(r["othc_aud"]),
                doc_aud=_to_float(r["doc_aud"]),
                cmr_aud=_to_float(r["cmr_aud"]),
                ams_usd=_to_float(r["ams_usd"]),
                lss_usd=_to_float(r["lss_usd"]),
                dthc=str(r["dthc"]).upper(),
                free_time=str(r["free_time"]),
                customer_id=customer.id,
            )

            if rate:
                for k, v in fields.items():
                    setattr(rate, k, v)
            else:
                session.add(Rate(**fields))

def seed_tariffs(session: OrmSession):
    if not TARIFF_JSON.exists():
        return

    data = json.loads(TARIFF_JSON.read_text())

    for t in data:
        tariff = session.query(Tariff).filter_by(
            load_port=t["load_port"],
            destination_port=t["destination_port"],
            container_type=t["container_type"],
        ).first()

        fields = dict(
            load_port=t["load_port"],
            destination_port=t["destination_port"],
            container_type=t["container_type"],
            freight_usd=_to_float(t["freight_usd"]),
            othc_aud=_to_float(t["othc_aud"]),
            doc_aud=_to_float(t["doc_aud"]),
            cmr_aud=_to_float(t["cmr_aud"]),
            ams_usd=_to_float(t["ams_usd"]),
            lss_usd=_to_float(t["lss_usd"]),
            dthc=str(t["dthc"]).upper(),
            free_time=str(t["free_time"]),
        )

        if tariff:
            for k, v in fields.items():
                setattr(tariff, k, v)
        else:
            session.add(Tariff(**fields))

def main():
    Base.metadata.create_all(engine)
    s = Session()
    try:
        seed_customers_and_rates(s)
        seed_tariffs(s)
        s.commit()
        print("Seed complete.")
    except Exception:
        s.rollback()
        raise
    finally:
        s.close()

if __name__ == "__main__":
    main()
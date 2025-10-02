from sqlalchemy import (
    create_engine, Column, Integer, String, Float, ForeignKey,
    CheckConstraint, UniqueConstraint
)
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

engine = create_engine("sqlite:///shipping.db", future=True)
Session = sessionmaker(bind=engine, future=True)
Base = declarative_base()

class Customer(Base):
    __tablename__ = "customers"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    email = Column(String)
    rates = relationship("Rate", back_populates="customer", cascade="all, delete-orphan")

class Rate(Base):
    __tablename__ = "rates"
    id = Column(Integer, primary_key=True)
    load_port = Column(String, nullable=False)
    destination_port = Column(String, nullable=False)
    container_type = Column(String, nullable=False)
    freight_usd = Column(Float, nullable=False)
    othc_aud = Column(Float, nullable=False)
    doc_aud = Column(Float, nullable=False)
    cmr_aud = Column(Float, nullable=False)
    ams_usd = Column(Float, nullable=False)
    lss_usd = Column(Float, nullable=False)
    dthc = Column(String, nullable=False)
    free_time = Column(String, nullable=False)

    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    customer = relationship("Customer", back_populates="rates")

    __table_args__ = (
        CheckConstraint("freight_usd >= 0", name="ck_freight_nonneg"),
        UniqueConstraint(
            "customer_id", "load_port", "destination_port", "container_type",
            name="uq_customer_lane_container"
        ),
    )

class Tariff(Base):
    __tablename__ = "tariffs"
    id = Column(Integer, primary_key=True)
    load_port = Column(String, nullable=False)
    destination_port = Column(String, nullable=False)
    container_type = Column(String, nullable=False)
    freight_usd = Column(Float, nullable=False)
    othc_aud = Column(Float, nullable=False)
    doc_aud = Column(Float, nullable=False)
    cmr_aud = Column(Float, nullable=False)
    ams_usd = Column(Float, nullable=False)
    lss_usd = Column(Float, nullable=False)
    dthc = Column(String, nullable=False)
    free_time = Column(String, nullable=False)
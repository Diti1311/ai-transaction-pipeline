from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Float
from sqlalchemy import Boolean

from app.core.database import Base


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True)

    job_id = Column(Integer)

    txn_id = Column(String, nullable=True)

    date = Column(String, nullable=True)

    merchant = Column(String, nullable=True)

    amount = Column(Float)

    currency = Column(String, nullable=True)

    status = Column(String, nullable=True)

    category = Column(String, nullable=True)

    account_id = Column(String, nullable=True)

    is_anomaly = Column(Boolean, default=False)

    anomaly_reason = Column(String, nullable=True)

    llm_category = Column(String, nullable=True)

    llm_raw_response = Column(String, nullable=True)

    llm_failed = Column(Boolean, default=False)
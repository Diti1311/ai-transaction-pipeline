from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Float
from sqlalchemy import Text
from app.core.database import Base


class Summary(Base):
    __tablename__ = "job_summaries"

    id = Column(Integer, primary_key=True)

    job_id = Column(Integer)

    total_spend_inr = Column(Float)

    total_spend_usd = Column(Float)

    top_merchants = Column(Text)

    anomaly_count = Column(Integer)

    narrative = Column(Text)

    risk_level = Column(String)
from sqlalchemy import Column, Integer, String, DateTime

from app.core.database import Base


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)

    filename = Column(String)
    file_path = Column(String, nullable=True)
    status = Column(String, default="pending")

    row_count_raw = Column(Integer, nullable=True)

    row_count_clean = Column(Integer, nullable=True)

    created_at = Column(DateTime)

    completed_at = Column(DateTime, nullable=True)

    error_message = Column(String, nullable=True)
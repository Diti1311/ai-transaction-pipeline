import time

from sqlalchemy import text

from app.core.database import engine
from app.core.database import Base

from app.models.job import Job
from app.models.transaction import Transaction
from app.models.summary import Summary


def init_db():

    retries = 10

    while retries:

        try:
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))

            Base.metadata.create_all(bind=engine)

            print("Database Connected")

            return

        except Exception as e:

            print(f"Waiting for database... {e}")

            retries -= 1

            time.sleep(3)

    raise Exception("Database unavailable")
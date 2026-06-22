from celery import Celery
from dotenv import load_dotenv
import os

load_dotenv()

REDIS_URL = os.getenv("REDIS_URL")

celery_app = Celery(
    "transaction_tasks",
    broker=REDIS_URL,
    backend=REDIS_URL,
    include=["app.workers.tasks"]
)
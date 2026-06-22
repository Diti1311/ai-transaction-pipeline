from datetime import datetime
import os
from fastapi import APIRouter
from fastapi import UploadFile
from fastapi import File
from fastapi import Depends

from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.job import Job
from app.workers.tasks import process_csv
from app.models.transaction import Transaction

router = APIRouter(
    prefix="/jobs",
    tags=["Jobs"]
)


@router.post("/upload")
async def upload_csv(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):

    os.makedirs("uploads", exist_ok=True)

    file_path = f"uploads/{file.filename}"

    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    job = Job(
        filename=file.filename,
        file_path=file_path,
        status="pending",
        created_at=datetime.utcnow()
    )

    db.add(job)
    db.commit()
    db.refresh(job)
    process_csv.delay(job.id)
    return {
        "job_id": job.id,
        "status": job.status
    }

@router.get("/{job_id}/status")
def get_job_status(
    job_id: int,
    db: Session = Depends(get_db)
):

    job = db.query(Job).filter(Job.id == job_id).first()

    if not job:
        return {
            "error": "Job not found"
        }

    return {
        "job_id": job.id,
        "status": job.status,
        "filename": job.filename,
        "rows_raw": job.row_count_raw,
        "rows_clean": job.row_count_clean,
        "error": job.error_message
    }

@router.get("/")
def get_all_jobs(
    db: Session = Depends(get_db)
):

    jobs = db.query(Job).all()

    return jobs

@router.get("/{job_id}/results")
def get_results(
    job_id: int,
    db: Session = Depends(get_db)
):

    transactions = (
        db.query(Transaction)
        .filter(Transaction.job_id == job_id)
        .all()
    )

    results = []

    for txn in transactions:

        results.append({
            "txn_id": txn.txn_id,
            "merchant": txn.merchant,
            "amount": txn.amount,
            "category": txn.category,
            "is_anomaly": txn.is_anomaly
        })

    return results
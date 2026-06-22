from datetime import datetime

from app.workers.celery_worker import celery_app

from app.core.database import SessionLocal

from app.models.job import Job
from app.models.transaction import Transaction
from app.models.summary import Summary

from app.services.csv_processor import load_and_clean_csv
from app.services.anomaly_detector import detect_anomalies

from app.services.gemini_service import classify_merchants
from app.services.summary_service import generate_summary

from app.services.llm_utils import retry_llm


@celery_app.task
def process_csv(job_id):

    db = SessionLocal()

    try:

        job = (
            db.query(Job)
            .filter(Job.id == job_id)
            .first()
        )

        if not job:
            return

        # -----------------------
        # Mark Processing
        # -----------------------

        job.status = "processing"
        db.commit()

        # -----------------------
        # Load + Clean CSV
        # -----------------------

        df, raw_count, clean_count = (
            load_and_clean_csv(
                job.file_path
            )
        )

        # -----------------------
        # Anomaly Detection
        # -----------------------

        anomaly_map = detect_anomalies(df)

        # -----------------------
        # Gemini Categorization
        # -----------------------

        missing_categories = df[
            df["category"].str.strip() == ""
        ]

        merchant_list = (
            missing_categories["merchant"]
            .dropna()
            .unique()
            .tolist()
        )

        classifications = {}

        llm_result = retry_llm(
            classify_merchants,
            merchant_list
        )

        if llm_result:
            classifications = llm_result

        # -----------------------
        # Save Transactions
        # -----------------------

        for idx, row in df.iterrows():

            category = row["category"]

            if not category:

                category = classifications.get(
                    row["merchant"],
                    "Other"
                )

            reasons = anomaly_map.get(
                idx,
                []
            )

            transaction = Transaction(

                job_id=job.id,

                txn_id=str(
                    row.get("txn_id", "")
                ),

                date=str(
                    row.get("date", "")
                ),

                merchant=str(
                    row.get("merchant", "")
                ),

                amount=float(
                    row.get("amount", 0)
                ),

                currency=str(
                    row.get("currency", "")
                ),

                status=str(
                    row.get("status", "")
                ),

                category=category,

                account_id=str(
                    row.get("account_id", "")
                ),

                is_anomaly=len(reasons) > 0,

                anomaly_reason=", ".join(
                    reasons
                ),

                llm_category=category,

                llm_failed=(
                    llm_result is None
                )
            )

            db.add(transaction)

        db.commit()

        # -----------------------
        # Build Summary Payload
        # -----------------------

        total_spend_inr = float(
            df[
                df["currency"] == "INR"
            ]["amount"].sum()
        )

        total_spend_usd = float(
            df[
                df["currency"] == "USD"
            ]["amount"].sum()
        )

        top_merchants = (
            df["merchant"]
            .value_counts()
            .head(3)
            .to_dict()
        )

        summary_payload = {

            "total_spend_inr":
                total_spend_inr,

            "total_spend_usd":
                total_spend_usd,

            "top_merchants":
                top_merchants,

            "anomaly_count":
                len(anomaly_map)
        }

        # -----------------------
        # Gemini Narrative Summary
        # -----------------------

        summary_result = retry_llm(
            generate_summary,
            summary_payload
        )

        # -----------------------
        # Save Summary
        # -----------------------

        if summary_result:

            summary = Summary(

                job_id=job.id,

                total_spend_inr=
                    summary_result.get(
                        "total_spend_inr",
                        total_spend_inr
                    ),

                total_spend_usd=
                    summary_result.get(
                        "total_spend_usd",
                        total_spend_usd
                    ),

                top_merchants=str(
                    summary_result.get(
                        "top_merchants",
                        top_merchants
                    )
                ),

                anomaly_count=
                    summary_result.get(
                        "anomaly_count",
                        len(anomaly_map)
                    ),

                narrative=
                    summary_result.get(
                        "narrative",
                        ""
                    ),

                risk_level=
                    summary_result.get(
                        "risk_level",
                        "low"
                    )
            )

        else:

            summary = Summary(

                job_id=job.id,

                total_spend_inr=
                    total_spend_inr,

                total_spend_usd=
                    total_spend_usd,

                top_merchants=
                    str(top_merchants),

                anomaly_count=
                    len(anomaly_map),

                narrative=
                    "LLM summary generation failed",

                risk_level=
                    "unknown"
            )

        db.add(summary)

        # -----------------------
        # Update Job
        # -----------------------

        job.row_count_raw = raw_count

        job.row_count_clean = clean_count

        job.status = "completed"

        job.completed_at = (
            datetime.utcnow()
        )

        db.commit()

        print(
            f"Job {job_id} completed"
        )

    except Exception as e:

        print(
            f"Job {job_id} failed: {e}"
        )

        try:

            job = (
                db.query(Job)
                .filter(Job.id == job_id)
                .first()
            )

            if job:

                job.status = "failed"

                job.error_message = str(e)

                db.commit()

        except Exception:
            pass

    finally:

        db.close()
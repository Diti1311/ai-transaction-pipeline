from app.models.transaction import Transaction


def save_transactions(df, job_id, db):

    for _, row in df.iterrows():

        transaction = Transaction(
            job_id=job_id,
            txn_id=str(row.get("txn_id", "")),
            date=str(row.get("date", "")),
            merchant=str(row.get("merchant", "")),
            amount=float(row.get("amount", 0)),
            currency=str(row.get("currency", "")),
            status=str(row.get("status", "")),
            category=str(row.get("category", "")),
            account_id=str(row.get("account_id", ""))
        )

        db.add(transaction)

    db.commit()
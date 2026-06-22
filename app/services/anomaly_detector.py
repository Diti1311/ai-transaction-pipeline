DOMESTIC_ONLY = {
    "SWIGGY",
    "OLA",
    "IRCTC"
}


def detect_anomalies(df):

    anomaly_map = {}

    medians = (
        df.groupby("account_id")["amount"]
        .median()
        .to_dict()
    )

    for idx, row in df.iterrows():

        reasons = []

        account_id = row["account_id"]

        median = medians.get(account_id)

        if median and row["amount"] > (3 * median):
            reasons.append(
                "Amount exceeds 3x account median"
            )

        merchant = str(
            row["merchant"]
        ).upper()

        currency = str(
            row["currency"]
        ).upper()

        if (
            currency == "USD"
            and merchant in DOMESTIC_ONLY
        ):
            reasons.append(
                "USD used with domestic-only merchant"
            )

        if reasons:
            anomaly_map[idx] = reasons

    return anomaly_map
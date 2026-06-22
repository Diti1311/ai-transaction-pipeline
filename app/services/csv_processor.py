import pandas as pd


def normalize_dates(date_value):

    try:
        return pd.to_datetime(
            date_value,
            dayfirst=True
        ).strftime("%Y-%m-%d")

    except Exception:
        return None


def clean_dataframe(df):

    raw_count = len(df)

    # Remove exact duplicates
    df = df.drop_duplicates()

    # Normalize dates
    df["date"] = df["date"].apply(normalize_dates)

    # Remove $
    df["amount"] = (
        df["amount"]
        .astype(str)
        .str.replace("$", "", regex=False)
    )

    df["amount"] = pd.to_numeric(
        df["amount"],
        errors="coerce"
    )

    # Uppercase status
    df["status"] = (
        df["status"]
        .astype(str)
        .str.upper()
    )

    # Currency uppercase
    df["currency"] = (
        df["currency"]
        .astype(str)
        .str.upper()
    )

    # Keep blanks for Gemini later
    df["category"] = (
        df["category"]
        .fillna("")
        .astype(str)
    )

    clean_count = len(df)

    return df, raw_count, clean_count


def load_and_clean_csv(file_path):

    df = pd.read_csv(file_path)

    return clean_dataframe(df)
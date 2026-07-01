import re
from pathlib import Path

import pandas as pd


RAW_DATA_PATH = Path("data/sample_reviews.csv")
CLEAN_DATA_PATH = Path("data/cleaned_reviews.csv")


def clean_text(text: str) -> str:
    """Lowercase review text and remove extra spaces/special characters."""
    text = str(text).lower().strip()
    text = re.sub(r"[^a-z0-9\s.,!?'-]", "", text)
    text = re.sub(r"\s+", " ", text)
    return text


def clean_reviews(input_path: Path = RAW_DATA_PATH, output_path: Path = CLEAN_DATA_PATH) -> pd.DataFrame:
    """Load, clean, and save beauty product review data."""
    df = pd.read_csv(input_path)

    df = df.dropna(subset=["review_id", "product_name", "rating", "review_text"])
    df["rating"] = pd.to_numeric(df["rating"], errors="coerce")
    df = df.dropna(subset=["rating"])
    df["rating"] = df["rating"].astype(int)

    df["review_date"] = pd.to_datetime(df["review_date"], errors="coerce")
    df["clean_review_text"] = df["review_text"].apply(clean_text)
    df["review_length"] = df["clean_review_text"].str.split().str.len()

    df = df.sort_values(["review_date", "product_name"]).reset_index(drop=True)
    df.to_csv(output_path, index=False)

    return df


if __name__ == "__main__":
    cleaned = clean_reviews()
    print(f"Cleaned {len(cleaned)} reviews.")
    print(f"Saved cleaned data to {CLEAN_DATA_PATH}")

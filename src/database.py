import sqlite3
from pathlib import Path

import pandas as pd


SENTIMENT_DATA_PATH = Path("outputs/review_sentiment.csv")
DATABASE_PATH = Path("outputs/beauty_reviews.db")
SCHEMA_PATH = Path("sql/schema.sql")


def create_database() -> None:
    """Create a SQLite database and load sentiment-labeled beauty review data."""
    df = pd.read_csv(SENTIMENT_DATA_PATH)

    with sqlite3.connect(DATABASE_PATH) as conn:
        schema_sql = SCHEMA_PATH.read_text()
        conn.executescript(schema_sql)

        df.to_sql(
            "beauty_reviews",
            conn,
            if_exists="append",
            index=False
        )

    print(f"Loaded {len(df)} reviews into {DATABASE_PATH}")


if __name__ == "__main__":
    create_database()

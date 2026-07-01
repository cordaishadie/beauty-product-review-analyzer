from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


SENTIMENT_DATA_PATH = Path("outputs/review_sentiment.csv")
PRODUCT_INSIGHTS_PATH = Path("outputs/product_insights.csv")
SENTIMENT_SUMMARY_PATH = Path("outputs/sentiment_summary.csv")
COMPLAINT_SUMMARY_PATH = Path("outputs/complaint_summary.csv")

SCREENSHOTS_DIR = Path("screenshots")


def load_review_data(path: Path = SENTIMENT_DATA_PATH) -> pd.DataFrame:
    """Load sentiment-labeled beauty review data."""
    return pd.read_csv(path)


def create_product_insights(df: pd.DataFrame) -> pd.DataFrame:
    """Create product-level review performance metrics."""
    product_summary = (
        df.groupby(["product_name", "category"])
        .agg(
            review_count=("review_id", "count"),
            average_rating=("rating", "mean"),
            average_review_length=("review_length", "mean"),
            negative_review_count=("sentiment", lambda x: (x == "negative").sum()),
            positive_review_count=("sentiment", lambda x: (x == "positive").sum()),
        )
        .reset_index()
    )

    product_summary["negative_review_rate"] = (
        product_summary["negative_review_count"] / product_summary["review_count"]
    ).round(2)

    product_summary["average_rating"] = product_summary["average_rating"].round(2)
    product_summary["average_review_length"] = product_summary["average_review_length"].round(1)

    product_summary = product_summary.sort_values(
        ["average_rating", "positive_review_count"], ascending=False
    )

    return product_summary


def create_sentiment_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Summarize sentiment distribution across reviews."""
    sentiment_summary = (
        df["sentiment"]
        .value_counts()
        .rename_axis("sentiment")
        .reset_index(name="review_count")
    )

    sentiment_summary["percentage"] = (
        sentiment_summary["review_count"] / sentiment_summary["review_count"].sum() * 100
    ).round(1)

    return sentiment_summary


def create_complaint_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Summarize complaint categories from non-positive reviews."""
    complaints = df[df["complaint_category"] != "none"]

    complaint_summary = (
        complaints["complaint_category"]
        .value_counts()
        .rename_axis("complaint_category")
        .reset_index(name="review_count")
    )

    return complaint_summary


def save_sentiment_chart(sentiment_summary: pd.DataFrame) -> None:
    """Save a sentiment distribution chart."""
    plt.figure(figsize=(8, 5))
    plt.bar(sentiment_summary["sentiment"], sentiment_summary["review_count"])
    plt.title("Beauty Review Sentiment Distribution")
    plt.xlabel("Sentiment")
    plt.ylabel("Number of Reviews")
    plt.tight_layout()
    plt.savefig(SCREENSHOTS_DIR / "sentiment_distribution.png")
    plt.close()


def save_rating_chart(product_summary: pd.DataFrame) -> None:
    """Save an average rating by product chart."""
    plt.figure(figsize=(10, 5))
    plt.bar(product_summary["product_name"], product_summary["average_rating"])
    plt.title("Average Rating by Beauty Product")
    plt.xlabel("Product")
    plt.ylabel("Average Rating")
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()
    plt.savefig(SCREENSHOTS_DIR / "average_rating_by_product.png")
    plt.close()


def save_complaint_chart(complaint_summary: pd.DataFrame) -> None:
    """Save a complaint category chart."""
    plt.figure(figsize=(8, 5))
    plt.bar(complaint_summary["complaint_category"], complaint_summary["review_count"])
    plt.title("Common Beauty Product Complaint Categories")
    plt.xlabel("Complaint Category")
    plt.ylabel("Number of Reviews")
    plt.tight_layout()
    plt.savefig(SCREENSHOTS_DIR / "complaint_categories.png")
    plt.close()


def main() -> None:
    """Generate product insights, summary tables, and charts."""
    SCREENSHOTS_DIR.mkdir(exist_ok=True)
    Path("outputs").mkdir(exist_ok=True)

    df = load_review_data()

    product_summary = create_product_insights(df)
    sentiment_summary = create_sentiment_summary(df)
    complaint_summary = create_complaint_summary(df)

    product_summary.to_csv(PRODUCT_INSIGHTS_PATH, index=False)
    sentiment_summary.to_csv(SENTIMENT_SUMMARY_PATH, index=False)
    complaint_summary.to_csv(COMPLAINT_SUMMARY_PATH, index=False)

    save_sentiment_chart(sentiment_summary)
    save_rating_chart(product_summary)
    save_complaint_chart(complaint_summary)

    print("Review insights generated successfully.")
    print(f"Saved product insights to {PRODUCT_INSIGHTS_PATH}")
    print(f"Saved sentiment summary to {SENTIMENT_SUMMARY_PATH}")
    print(f"Saved complaint summary to {COMPLAINT_SUMMARY_PATH}")
    print(f"Saved charts to {SCREENSHOTS_DIR}")


if __name__ == "__main__":
    main()

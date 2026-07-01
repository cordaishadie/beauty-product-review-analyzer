from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


SENTIMENT_DATA_PATH = Path("outputs/review_sentiment.csv")
PRODUCT_INSIGHTS_PATH = Path("outputs/product_insights.csv")
SENTIMENT_SUMMARY_PATH = Path("outputs/sentiment_summary.csv")
COMPLAINT_SUMMARY_PATH = Path("outputs/complaint_summary.csv")
MONTHLY_SENTIMENT_PATH = Path("outputs/monthly_sentiment_trend.csv")

SCREENSHOTS_DIR = Path("screenshots")


def load_review_data(path: Path = SENTIMENT_DATA_PATH) -> pd.DataFrame:
    return pd.read_csv(path)


def create_product_insights(df: pd.DataFrame) -> pd.DataFrame:
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

    return product_summary.sort_values(
        ["average_rating", "positive_review_count"], ascending=False
    )


def create_sentiment_summary(df: pd.DataFrame) -> pd.DataFrame:
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
    complaints = df[df["complaint_category"] != "none"]

    if complaints.empty:
        return pd.DataFrame(columns=["complaint_category", "review_count"])

    return (
        complaints["complaint_category"]
        .value_counts()
        .rename_axis("complaint_category")
        .reset_index(name="review_count")
    )


def create_monthly_sentiment_trend(df: pd.DataFrame) -> pd.DataFrame:
    trend_df = df.copy()
    trend_df["review_date"] = pd.to_datetime(trend_df["review_date"])
    trend_df["month"] = trend_df["review_date"].dt.to_period("M").astype(str)

    return (
        trend_df.groupby(["month", "sentiment"])
        .size()
        .reset_index(name="review_count")
        .sort_values(["month", "sentiment"])
    )


def save_sentiment_chart(sentiment_summary: pd.DataFrame) -> None:
    plt.figure(figsize=(8, 5))
    plt.bar(sentiment_summary["sentiment"], sentiment_summary["review_count"])
    plt.title("Beauty Review Sentiment Distribution")
    plt.xlabel("Sentiment")
    plt.ylabel("Number of Reviews")
    plt.tight_layout()
    plt.savefig(SCREENSHOTS_DIR / "sentiment_distribution.png")
    plt.close()


def save_rating_chart(product_summary: pd.DataFrame) -> None:
    plt.figure(figsize=(11, 6))
    plt.bar(product_summary["product_name"], product_summary["average_rating"])
    plt.title("Average Rating by Beauty Product")
    plt.xlabel("Product")
    plt.ylabel("Average Rating")
    plt.xticks(rotation=35, ha="right")
    plt.tight_layout()
    plt.savefig(SCREENSHOTS_DIR / "average_rating_by_product.png")
    plt.close()


def save_complaint_chart(complaint_summary: pd.DataFrame) -> None:
    if complaint_summary.empty:
        return

    plt.figure(figsize=(8, 5))
    plt.bar(complaint_summary["complaint_category"], complaint_summary["review_count"])
    plt.title("Common Beauty Product Complaint Categories")
    plt.xlabel("Complaint Category")
    plt.ylabel("Number of Reviews")
    plt.tight_layout()
    plt.savefig(SCREENSHOTS_DIR / "complaint_categories.png")
    plt.close()


def save_monthly_sentiment_chart(monthly_trend: pd.DataFrame) -> None:
    pivot = monthly_trend.pivot(index="month", columns="sentiment", values="review_count").fillna(0)

    plt.figure(figsize=(10, 5))
    for sentiment in pivot.columns:
        plt.plot(pivot.index, pivot[sentiment], marker="o", label=sentiment)

    plt.title("Monthly Review Sentiment Trend")
    plt.xlabel("Month")
    plt.ylabel("Number of Reviews")
    plt.xticks(rotation=30, ha="right")
    plt.legend()
    plt.tight_layout()
    plt.savefig(SCREENSHOTS_DIR / "monthly_sentiment_trend.png")
    plt.close()


def save_dashboard_preview(
    df: pd.DataFrame,
    product_summary: pd.DataFrame,
    sentiment_summary: pd.DataFrame,
    complaint_summary: pd.DataFrame,
) -> None:
    total_reviews = len(df)
    average_rating = round(df["rating"].mean(), 2)
    positive_rate = round((df["sentiment"].eq("positive").mean()) * 100, 1)
    top_product = product_summary.iloc[0]["product_name"]
    top_complaint = (
        complaint_summary.iloc[0]["complaint_category"]
        if not complaint_summary.empty
        else "none"
    )

    fig = plt.figure(figsize=(12, 7))
    fig.suptitle("Beauty Review Analytics Dashboard Preview", fontsize=16)

    ax1 = fig.add_subplot(2, 2, 1)
    ax1.axis("off")
    kpi_text = (
        f"Total reviews: {total_reviews}\n"
        f"Average rating: {average_rating}\n"
        f"Positive review rate: {positive_rate}%\n"
        f"Top rated product: {top_product}\n"
        f"Top complaint: {top_complaint}"
    )
    ax1.text(0.05, 0.65, kpi_text, fontsize=12, va="top")

    ax2 = fig.add_subplot(2, 2, 2)
    ax2.bar(sentiment_summary["sentiment"], sentiment_summary["review_count"])
    ax2.set_title("Sentiment Mix")
    ax2.set_ylabel("Reviews")

    ax3 = fig.add_subplot(2, 2, 3)
    ax3.bar(product_summary["product_name"], product_summary["average_rating"])
    ax3.set_title("Average Rating by Product")
    ax3.tick_params(axis="x", rotation=45)

    ax4 = fig.add_subplot(2, 2, 4)
    if not complaint_summary.empty:
        ax4.bar(complaint_summary["complaint_category"], complaint_summary["review_count"])
        ax4.set_title("Complaint Categories")
        ax4.tick_params(axis="x", rotation=30)
    else:
        ax4.axis("off")
        ax4.text(0.1, 0.5, "No complaint categories detected")

    plt.tight_layout()
    plt.savefig(SCREENSHOTS_DIR / "dashboard_preview.png")
    plt.close()


def main() -> None:
    SCREENSHOTS_DIR.mkdir(exist_ok=True)
    Path("outputs").mkdir(exist_ok=True)

    df = load_review_data()

    product_summary = create_product_insights(df)
    sentiment_summary = create_sentiment_summary(df)
    complaint_summary = create_complaint_summary(df)
    monthly_trend = create_monthly_sentiment_trend(df)

    product_summary.to_csv(PRODUCT_INSIGHTS_PATH, index=False)
    sentiment_summary.to_csv(SENTIMENT_SUMMARY_PATH, index=False)
    complaint_summary.to_csv(COMPLAINT_SUMMARY_PATH, index=False)
    monthly_trend.to_csv(MONTHLY_SENTIMENT_PATH, index=False)

    save_sentiment_chart(sentiment_summary)
    save_rating_chart(product_summary)
    save_complaint_chart(complaint_summary)
    save_monthly_sentiment_chart(monthly_trend)
    save_dashboard_preview(df, product_summary, sentiment_summary, complaint_summary)

    print("Review insights generated successfully.")
    print(f"Saved product insights to {PRODUCT_INSIGHTS_PATH}")
    print(f"Saved sentiment summary to {SENTIMENT_SUMMARY_PATH}")
    print(f"Saved complaint summary to {COMPLAINT_SUMMARY_PATH}")
    print(f"Saved monthly sentiment trend to {MONTHLY_SENTIMENT_PATH}")
    print(f"Saved charts to {SCREENSHOTS_DIR}")


if __name__ == "__main__":
    main()

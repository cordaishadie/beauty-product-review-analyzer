from pathlib import Path

import pandas as pd


CLEAN_DATA_PATH = Path("data/cleaned_reviews.csv")
SENTIMENT_OUTPUT_PATH = Path("outputs/review_sentiment.csv")


POSITIVE_WORDS = {
    "love", "glow", "brighter", "hydrating", "soft", "smooth", "clean",
    "moisturizing", "lightweight", "perfect", "repaired", "repurchase",
    "helped", "great", "good", "absorbs"
}

NEGATIVE_WORDS = {
    "irritated", "bumps", "drying", "tight", "heavy", "greasy", "broke",
    "leaked", "sticky", "overpriced", "no results", "dry", "clog"
}

COMPLAINT_KEYWORDS = {
    "irritation": ["irritated", "bumps", "broke me out"],
    "dryness": ["dry", "drying", "tight"],
    "texture": ["heavy", "greasy", "sticky"],
    "packaging": ["packaging", "tube", "leaked", "melted"],
    "value": ["overpriced", "no results"],
}


def score_sentiment(text: str, rating: int) -> str:
    """Classify sentiment using rating signals and keyword matching."""
    text = str(text).lower()

    positive_matches = sum(1 for word in POSITIVE_WORDS if word in text)
    negative_matches = sum(1 for word in NEGATIVE_WORDS if word in text)

    if rating >= 4 and positive_matches >= negative_matches:
        return "positive"

    if rating <= 2 or negative_matches > positive_matches:
        return "negative"

    return "neutral"


def detect_complaint_category(text: str, sentiment: str) -> str:
    """Detect the most relevant customer complaint category."""
    text = str(text).lower()

    if sentiment == "positive":
        return "none"

    if "without feeling greasy" in text or "does not clog" in text:
        return "none"

    for category, keywords in COMPLAINT_KEYWORDS.items():
        if any(keyword in text for keyword in keywords):
            return category

    return "none"


def add_sentiment_labels(
    input_path: Path = CLEAN_DATA_PATH,
    output_path: Path = SENTIMENT_OUTPUT_PATH
) -> pd.DataFrame:
    """Add sentiment and complaint categories to cleaned review data."""
    df = pd.read_csv(input_path)

    df["sentiment"] = df.apply(
        lambda row: score_sentiment(row["clean_review_text"], row["rating"]),
        axis=1
    )

    df["complaint_category"] = df.apply(
        lambda row: detect_complaint_category(row["clean_review_text"], row["sentiment"]),
        axis=1
    )

    df.to_csv(output_path, index=False)
    return df


if __name__ == "__main__":
    sentiment_df = add_sentiment_labels()
    print("Sentiment analysis complete.")
    print(sentiment_df[["product_name", "rating", "sentiment", "complaint_category"]].head())
    print(f"Saved sentiment output to {SENTIMENT_OUTPUT_PATH}")

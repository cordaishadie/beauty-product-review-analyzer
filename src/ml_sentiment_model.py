from pathlib import Path

import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline


CLEAN_DATA_PATH = Path("data/cleaned_reviews.csv")
MODEL_PATH = Path("outputs/ml_sentiment_model.joblib")
METRICS_PATH = Path("outputs/ml_model_metrics.txt")
PREDICTIONS_PATH = Path("outputs/ml_sentiment_predictions.csv")


def rating_to_label(rating: int) -> str:
    if rating >= 4:
        return "positive"
    if rating <= 2:
        return "negative"
    return "neutral"


def train_model() -> None:
    df = pd.read_csv(CLEAN_DATA_PATH)
    df["target_sentiment"] = df["rating"].apply(rating_to_label)

    x_train, x_test, y_train, y_test = train_test_split(
        df["clean_review_text"],
        df["target_sentiment"],
        test_size=0.25,
        random_state=42,
        stratify=df["target_sentiment"],
    )

    model = Pipeline(
        steps=[
            (
                "tfidf",
                TfidfVectorizer(
                    lowercase=True,
                    stop_words="english",
                    ngram_range=(1, 2),
                    min_df=1,
                ),
            ),
            (
                "classifier",
                LogisticRegression(max_iter=1000),
            ),
        ]
    )

    model.fit(x_train, y_train)
    predictions = model.predict(x_test)

    accuracy = accuracy_score(y_test, predictions)
    report = classification_report(y_test, predictions)

    metrics_text = (
        "ML Sentiment Model Report\n"
        "=========================\n\n"
        "Model: TF-IDF + Logistic Regression\n"
        f"Test accuracy: {accuracy:.2f}\n\n"
        "Classification report:\n"
        f"{report}\n"
    )

    METRICS_PATH.write_text(metrics_text)
    joblib.dump(model, MODEL_PATH)

    prediction_output = pd.DataFrame(
        {
            "review_text": x_test.values,
            "actual_sentiment": y_test.values,
            "predicted_sentiment": predictions,
        }
    )
    prediction_output.to_csv(PREDICTIONS_PATH, index=False)

    print(metrics_text)
    print(f"Saved model to {MODEL_PATH}")
    print(f"Saved metrics to {METRICS_PATH}")
    print(f"Saved predictions to {PREDICTIONS_PATH}")


if __name__ == "__main__":
    train_model()

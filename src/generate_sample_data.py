from datetime import datetime, timedelta
from pathlib import Path
import random

import pandas as pd


OUTPUT_PATH = Path("data/sample_reviews.csv")
random.seed(42)


PRODUCTS = [
    ("GlowSkin Vitamin C Serum", "Serum"),
    ("HydraSoft Daily Moisturizer", "Moisturizer"),
    ("ClearPore Clay Mask", "Mask"),
    ("LuxeLip Repair Balm", "Lip Care"),
    ("BrightEye Caffeine Cream", "Eye Cream"),
    ("FreshFoam Gentle Cleanser", "Cleanser"),
    ("SunVeil Daily SPF", "Sunscreen"),
    ("BalanceDrop Hydrating Toner", "Toner"),
]


POSITIVE_REVIEWS = [
    "I love this product. It made my skin look brighter and more even.",
    "Very hydrating and lightweight. My skin feels soft all day.",
    "This gave me a healthy glow without feeling greasy.",
    "The texture is smooth and it absorbs quickly.",
    "I noticed better skin texture after using this consistently.",
    "This product feels gentle and works well under makeup.",
    "My skin looks fresh, smooth, and more balanced.",
    "I would definitely repurchase this because the results were good.",
]

NEUTRAL_REVIEWS = [
    "The product is okay, but I did not notice a major difference.",
    "It feels nice, but the results were not dramatic.",
    "The texture is fine, but I expected a little more.",
    "It worked for basic use, but I am not sure I would repurchase.",
    "The formula is decent, but it may depend on skin type.",
    "I liked parts of the product, but the results were average.",
]

NEGATIVE_REVIEWS = [
    "This irritated my skin and caused small bumps.",
    "The product felt heavy and greasy on my skin.",
    "It was too drying and left my face feeling tight.",
    "I saw no results and the product felt overpriced.",
    "The packaging leaked and made the product messy to use.",
    "The formula felt sticky and uncomfortable.",
    "It broke me out after a few uses.",
    "This did not work well for my skin and felt harsh.",
]


def build_review_text(sentiment: str) -> str:
    if sentiment == "positive":
        return random.choice(POSITIVE_REVIEWS)
    if sentiment == "neutral":
        return random.choice(NEUTRAL_REVIEWS)
    return random.choice(NEGATIVE_REVIEWS)


def build_rating(sentiment: str) -> int:
    if sentiment == "positive":
        return random.choice([4, 5, 5])
    if sentiment == "neutral":
        return 3
    return random.choice([1, 2, 2])


def generate_reviews(review_count: int = 120) -> pd.DataFrame:
    start_date = datetime(2026, 1, 1)
    rows = []

    for review_id in range(1, review_count + 1):
        product_name, category = random.choice(PRODUCTS)
        sentiment = random.choices(
            ["positive", "neutral", "negative"],
            weights=[0.50, 0.20, 0.30],
            k=1,
        )[0]

        rows.append(
            {
                "review_id": review_id,
                "product_name": product_name,
                "category": category,
                "rating": build_rating(sentiment),
                "review_text": build_review_text(sentiment),
                "review_date": (start_date + timedelta(days=random.randint(0, 150))).date(),
            }
        )

    return pd.DataFrame(rows).sort_values("review_id")


if __name__ == "__main__":
    OUTPUT_PATH.parent.mkdir(exist_ok=True)
    reviews = generate_reviews()
    reviews.to_csv(OUTPUT_PATH, index=False)
    print(f"Generated {len(reviews)} sample beauty reviews.")
    print(f"Saved dataset to {OUTPUT_PATH}")

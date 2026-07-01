from pathlib import Path

import pandas as pd


PRODUCT_INSIGHTS_PATH = Path("outputs/product_insights.csv")
SENTIMENT_SUMMARY_PATH = Path("outputs/sentiment_summary.csv")
COMPLAINT_SUMMARY_PATH = Path("outputs/complaint_summary.csv")
RECOMMENDATIONS_PATH = Path("outputs/business_recommendations.md")


def main() -> None:
    product_insights = pd.read_csv(PRODUCT_INSIGHTS_PATH)
    sentiment_summary = pd.read_csv(SENTIMENT_SUMMARY_PATH)
    complaint_summary = pd.read_csv(COMPLAINT_SUMMARY_PATH)

    top_product = product_insights.sort_values("average_rating", ascending=False).iloc[0]
    risk_product = product_insights.sort_values("negative_review_rate", ascending=False).iloc[0]

    positive_row = sentiment_summary[sentiment_summary["sentiment"] == "positive"]
    positive_rate = (
        float(positive_row.iloc[0]["percentage"])
        if not positive_row.empty
        else 0.0
    )

    if not complaint_summary.empty:
        top_complaint = complaint_summary.iloc[0]["complaint_category"]
        top_complaint_count = int(complaint_summary.iloc[0]["review_count"])
    else:
        top_complaint = "none"
        top_complaint_count = 0

    markdown = f"""# Business Recommendations

This document translates the beauty review analysis into product and customer experience recommendations.

## Executive Summary

The sample review analysis shows that customer feedback can be used to identify product strengths, product risks, and common complaint themes beyond star ratings alone.

## Key Findings

- Positive review rate: {positive_rate}%
- Highest-rated product: {top_product["product_name"]} with an average rating of {top_product["average_rating"]}
- Product with highest negative review rate: {risk_product["product_name"]} with a negative review rate of {risk_product["negative_review_rate"]}
- Most common complaint category: {top_complaint} ({top_complaint_count} reviews)

## Recommendations

### 1. Use positive review language in marketing

Positive reviews frequently mention benefits such as glow, hydration, smooth texture, and visible improvement. These phrases can be used to guide product messaging, paid social copy, and product detail page content.

### 2. Monitor products with higher negative review rates

Products with a higher negative review rate should be reviewed for formulation, product claims, usage instructions, or customer education opportunities.

### 3. Turn complaint categories into product feedback loops

Complaint categories such as dryness, texture, packaging, irritation, and value can help product and marketing teams identify whether dissatisfaction is related to formula, packaging, pricing, or expectation-setting.

### 4. Pair review sentiment with rating trends

Ratings alone do not always explain why customers feel a certain way. Sentiment and complaint analysis provide context that can help teams make better decisions.

## Business Impact

A beauty brand could use this type of analysis to:

- Improve product positioning
- Identify recurring customer pain points
- Prioritize product improvements
- Support customer experience decisions
- Strengthen product detail pages with customer-backed insights
"""

    RECOMMENDATIONS_PATH.write_text(markdown)
    print(f"Saved business recommendations to {RECOMMENDATIONS_PATH}")


if __name__ == "__main__":
    main()

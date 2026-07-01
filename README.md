# Beauty Product Review Analyzer

A Python, SQL, and NLP analytics project that analyzes beauty product reviews to uncover sentiment trends, common customer complaints, rating patterns, and product-level insights.

## Project Overview

This project simulates how a beauty brand could analyze customer review data to better understand product performance, customer satisfaction, and recurring product issues.

The project uses a sample beauty review dataset and applies data cleaning, sentiment analysis, complaint categorization, SQL querying, and dashboard-ready reporting outputs.

## Why I Built This

I built this project because I am interested in the intersection of beauty, consumer behavior, and data analytics. Beauty brands rely heavily on customer feedback, and review data can reveal patterns that are not always obvious from ratings alone.

This project shows how data can be used to translate customer comments into product insights that support marketing, product development, and customer experience decisions.

## Tools Used

* Python
* Pandas
* NumPy
* Matplotlib
* SQL
* SQLite
* Pytest

## Key Features

* Cleans raw beauty product review data
* Standardizes review text for analysis
* Classifies reviews as positive, neutral, or negative
* Detects complaint categories such as irritation, dryness, texture, packaging, and value
* Creates product-level performance metrics
* Loads review data into a SQLite database
* Generates dashboard-style charts
* Includes unit tests for data cleaning and sentiment logic

## Project Structure

```text
beauty-product-review-analyzer/
├── data/
│   ├── sample_reviews.csv
│   └── cleaned_reviews.csv
├── outputs/
│   ├── beauty_reviews.db
│   ├── review_sentiment.csv
│   ├── product_insights.csv
│   ├── sentiment_summary.csv
│   └── complaint_summary.csv
├── screenshots/
│   ├── sentiment_distribution.png
│   ├── average_rating_by_product.png
│   └── complaint_categories.png
├── sql/
│   ├── schema.sql
│   └── analysis_queries.sql
├── src/
│   ├── clean_reviews.py
│   ├── sentiment_analysis.py
│   ├── review_insights.py
│   └── database.py
└── tests/
    ├── test_clean_reviews.py
    └── test_sentiment_analysis.py
```

## Visual Outputs

### Sentiment Distribution

![Sentiment Distribution](screenshots/sentiment_distribution.png)

### Average Rating by Product

![Average Rating by Product](screenshots/average_rating_by_product.png)

### Complaint Categories

![Complaint Categories](screenshots/complaint_categories.png)

## Example Insights

Based on the sample dataset:

* Positive reviews often mention hydration, glow, softness, and smooth texture.
* Negative reviews often mention irritation, dryness, heaviness, greasiness, and lack of visible results.
* Complaint categories help separate general dissatisfaction from specific product issues.
* Product-level summaries make it easier to compare review count, average rating, and negative review rate.

## How to Run This Project

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Clean the review data:

```bash
python src/clean_reviews.py
```

Run sentiment analysis:

```bash
python src/sentiment_analysis.py
```

Generate insights and charts:

```bash
python src/review_insights.py
```

Create the SQLite database:

```bash
python src/database.py
```

Run tests:

```bash
python -m pytest
```

## SQL Analysis

The `sql/analysis_queries.sql` file includes queries for:

* Average rating by product
* Sentiment distribution
* Complaint category frequency
* Negative review rate by product

## Future Improvements

* Add a larger review dataset
* Use a transformer-based NLP model for more advanced sentiment classification
* Build an interactive Streamlit dashboard
* Add product category filters
* Connect the analysis to a cloud database
* Compare review trends across time periods

## Skills Demonstrated

* Data cleaning
* Exploratory data analysis
* Natural language processing
* SQL querying
* SQLite database creation
* Business insight generation
* Data visualization
* Python testing

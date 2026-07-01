DROP TABLE IF EXISTS beauty_reviews;

CREATE TABLE beauty_reviews (
    review_id INTEGER PRIMARY KEY,
    product_name TEXT NOT NULL,
    category TEXT NOT NULL,
    rating INTEGER NOT NULL,
    review_text TEXT NOT NULL,
    review_date TEXT,
    clean_review_text TEXT,
    review_length INTEGER,
    sentiment TEXT,
    complaint_category TEXT
);

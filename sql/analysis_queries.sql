-- Average rating and review count by product
SELECT
    product_name,
    category,
    COUNT(*) AS review_count,
    ROUND(AVG(rating), 2) AS average_rating
FROM beauty_reviews
GROUP BY product_name, category
ORDER BY average_rating DESC;

-- Sentiment distribution
SELECT
    sentiment,
    COUNT(*) AS review_count,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM beauty_reviews), 1) AS percentage
FROM beauty_reviews
GROUP BY sentiment
ORDER BY review_count DESC;

-- Complaint categories by frequency
SELECT
    complaint_category,
    COUNT(*) AS complaint_count
FROM beauty_reviews
WHERE complaint_category != 'none'
GROUP BY complaint_category
ORDER BY complaint_count DESC;

-- Products with highest negative review rate
SELECT
    product_name,
    COUNT(*) AS review_count,
    SUM(CASE WHEN sentiment = 'negative' THEN 1 ELSE 0 END) AS negative_reviews,
    ROUND(
        SUM(CASE WHEN sentiment = 'negative' THEN 1 ELSE 0 END) * 1.0 / COUNT(*),
        2
    ) AS negative_review_rate
FROM beauty_reviews
GROUP BY product_name
ORDER BY negative_review_rate DESC;

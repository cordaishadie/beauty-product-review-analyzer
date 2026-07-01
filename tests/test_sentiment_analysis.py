from src.sentiment_analysis import score_sentiment, detect_complaint_category


def test_positive_review_gets_positive_sentiment():
    text = "i love this product it gives my skin a glow"
    assert score_sentiment(text, 5) == "positive"


def test_negative_review_gets_negative_sentiment():
    text = "this irritated my skin and caused bumps"
    assert score_sentiment(text, 2) == "negative"


def test_detects_irritation_complaint():
    text = "this irritated my skin and caused bumps"
    assert detect_complaint_category(text, "negative") == "irritation"


def test_positive_review_has_no_complaint_category():
    text = "very hydrating without feeling greasy"
    assert detect_complaint_category(text, "positive") == "none"

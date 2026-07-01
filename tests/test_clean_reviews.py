from src.clean_reviews import clean_text


def test_clean_text_lowercases_review_text():
    text = "This Product Made My Skin GLOW!"
    assert clean_text(text) == "this product made my skin glow!"


def test_clean_text_removes_extra_spaces():
    text = "This    feels     amazing"
    assert clean_text(text) == "this feels amazing"

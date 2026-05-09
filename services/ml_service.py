import re

# =============================
# 🔹 LOAD MODEL
# =============================

def load_or_train():

    print("✅ Simple ML Model Loaded")


# =============================
# 🔹 CLEAN TEXT
# =============================

def clean_text(text: str):

    text = text.lower()

    text = re.sub(
        r'[^a-z\s]',
        '',
        text
    )

    return text.strip()


# =============================
# 🔹 PREDICT FUNCTION
# =============================

def predict_one(text: str):

    print(
        "🔥 FIXED ML RUNNING:",
        text
    )

    # EMPTY CHECK
    if not text or text.strip() == "":
        return "Neutral"

    text = clean_text(text)

    # POSITIVE
    positive_words = [

        "good",
        "great",
        "love",
        "amazing",
        "excellent",
        "awesome",
        "best",
        "happy"
    ]

    # NEGATIVE
    negative_words = [

        "bad",
        "hate",
        "terrible",
        "worst",
        "poor",
        "awful",
        "sad"
    ]

    # CHECK POSITIVE
    for word in positive_words:

        if word in text:
            return "Positive"

    # CHECK NEGATIVE
    for word in negative_words:

        if word in text:
            return "Negative"

    # DEFAULT
    return "Neutral"
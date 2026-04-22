import re

# =============================
# 🔹 CLEAN TEXT
# =============================
def clean_text(text: str):
    text = text.lower()
    text = re.sub(r'[^a-z\s]', '', text)
    return text.strip()


# =============================
# 🔹 PREDICT FUNCTION
# =============================
def predict_one(text: str):

    print("🔥 FIXED ML RUNNING:", text)

    # Empty check
    if not text or text.strip() == "":
        return "Neutral"

    text = clean_text(text)

    # ✅ POSITIVE
    if "good" in text or "great" in text or "love" in text or "amazing" in text:
        return "Positive"

    # ✅ NEGATIVE
    if "bad" in text or "hate" in text or "terrible" in text or "worst" in text:
        return "Negative"

    # ✅ DEFAULT
    return "Neutral"
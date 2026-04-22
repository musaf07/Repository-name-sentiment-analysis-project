import joblib
import re
import os

class SentimentAnalyzer:

    def __init__(self):
        print("🔥 SentimentAnalyzer initialized")

        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        model_path = os.path.join(BASE_DIR, "model.pkl")
        vectorizer_path = os.path.join(BASE_DIR, "vectorizer.pkl")

        self.model = joblib.load(model_path)
        self.vectorizer = joblib.load(vectorizer_path)

    # =============================
    # 🔹 CLEAN TEXT
    # =============================
    def clean_text(self, text):
        text = str(text).lower()
        text = re.sub(r'[^a-z\s]', '', text)
        return text.strip()

    # =============================
    # 🔹 RULE-BASED BOOST
    # =============================
    def rule_based(self, text):
        if any(word in text for word in ["bad", "worst", "hate", "terrible", "awful"]):
            return "Negative"
        if any(word in text for word in ["good", "great", "love", "excellent", "amazing"]):
            return "Positive"
        return None

    # =============================
    # 🔹 PREDICT
    # =============================
    def predict_sentiment(self, text):

        print("🚀 FUNCTION CALLED:", text)

        if not text or text.strip() == "":
            return {"sentiment": "Neutral", "confidence": 0.0}

        cleaned_text = self.clean_text(text)

        # 🔥 RULE FIRST
        rule = self.rule_based(cleaned_text)
        if rule:
            return {"sentiment": rule, "confidence": 0.99}

        # 🔥 VERY SHORT TEXT SAFETY
        if len(cleaned_text.split()) <= 1:
            return {"sentiment": "Neutral", "confidence": 0.5}

        # 🔥 ML PREDICTION
        vec = self.vectorizer.transform([cleaned_text])

        pred = self.model.predict(vec)[0]
        probs = self.model.predict_proba(vec)[0]

        confidence = float(max(probs))

        print("ML RAW:", pred, "| CONF:", confidence)

        # 🔥 MAP LABEL
        if pred == 2:
            sentiment = "Positive"
        elif pred == 1:
            sentiment = "Neutral"
        else:
            sentiment = "Negative"

        return {
            "sentiment": sentiment,
            "confidence": round(confidence, 2)
        }
import random
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()

# =====================================
# 📡 FAKE SOCIAL POSTS
# =====================================
posts = [

    "This product is amazing",
    "Worst update ever",
    "Excellent performance",
    "Battery drains fast",
    "Very happy with this service",
    "Terrible customer support",
    "Fantastic design",
    "I hate this app",
    "Best purchase ever",
    "Very disappointing experience",

    "Camera quality is awesome",
    "Network issue again",
    "I love this phone",
    "Slow response from support",
    "Absolutely fantastic",
    "Bad battery life",
]

# =====================================
# 🧠 ANALYZE
# =====================================
def analyze(text):

    score = analyzer.polarity_scores(text)["compound"]

    if score >= 0.05:
        sentiment = "Positive"
    elif score <= -0.05:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"

    return {
        "text": text,
        "sentiment": sentiment,
        "score": score
    }

# =====================================
# 🚀 GENERATE LIVE DATA
# =====================================
def get_live_data():

    text = random.choice(posts)

    return analyze(text)
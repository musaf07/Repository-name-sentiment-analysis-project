# ============================================
# 🚀 product_engine.py
# REAL PRODUCT INTELLIGENCE ENGINE
# ============================================

from vaderSentiment.vaderSentiment import (
    SentimentIntensityAnalyzer
)

from pytrends.request import TrendReq

import praw

# ============================================
# 🧠 AI MODEL
# ============================================
analyzer = SentimentIntensityAnalyzer()

# ============================================
# 📈 GOOGLE TRENDS
# ============================================
pytrend = TrendReq()

# ============================================
# 📡 REDDIT API
# ============================================
reddit = praw.Reddit(

    client_id="YOUR_CLIENT_ID",

    client_secret="YOUR_CLIENT_SECRET",

    user_agent="sentiment_dashboard"
)

# ============================================
# 🛒 PRODUCTS
# ============================================
products = {

    "iphone 15": {
        "alternatives": [
            "Samsung S24 Ultra",
            "Google Pixel 9",
            "OnePlus 12"
        ]
    },

    "samsung s24 ultra": {
        "alternatives": [
            "iPhone 15",
            "Xiaomi 14 Ultra",
            "Pixel 9 Pro"
        ]
    },

    "playstation 5": {
        "alternatives": [
            "Xbox Series X",
            "Nintendo Switch"
        ]
    },

    "macbook pro m3": {
        "alternatives": [
            "Dell XPS 15",
            "ASUS ROG Zephyrus"
        ]
    }
}

# ============================================
# 🔍 SENTIMENT
# ============================================
def analyze_sentiment(text):

    score = analyzer.polarity_scores(
        text
    )["compound"]

    if score >= 0.05:
        return "Positive", score

    elif score <= -0.05:
        return "Negative", score

    else:
        return "Neutral", score


# ============================================
# 📡 FETCH REDDIT POSTS
# ============================================
def fetch_reddit_posts(product):

    posts = []

    try:

        subreddit = reddit.subreddit("all")

        for post in subreddit.search(
            product,
            limit=20
        ):

            posts.append({

                "platform": "Reddit",

                "text": post.title
            })

    except Exception as e:

        print("Reddit Error:", e)

    return posts


# ============================================
# 📈 GOOGLE TREND SCORE
# ============================================
def get_trend_score(product):

    try:

        kw_list = [product]

        pytrend.build_payload(
            kw_list,
            timeframe='today 3-m'
        )

        data = pytrend.interest_over_time()

        if not data.empty:

            return int(
                data[product].mean()
            )

    except Exception as e:

        print("Trend Error:", e)

    return 50


# ============================================
# 🚀 MAIN PRODUCT ANALYSIS
# ============================================
def analyze_product(product):

    product = product.lower()

    # ====================================
    # PRODUCT CHECK
    # ====================================
    if product not in products:

        return {
            "error": "Product not found"
        }

    # ====================================
    # FETCH LIVE POSTS
    # ====================================
    posts = fetch_reddit_posts(product)

    # ====================================
    # TREND SCORE
    # ====================================
    trend_score = get_trend_score(
        product
    )

    # ====================================
    # COUNTERS
    # ====================================
    positive = 0
    negative = 0
    neutral = 0

    # ====================================
    # ANALYZE POSTS
    # ====================================
    for p in posts:

        sentiment, score = analyze_sentiment(
            p["text"]
        )

        if sentiment == "Positive":

            positive += 1

        elif sentiment == "Negative":

            negative += 1

        else:

            neutral += 1

    # ====================================
    # TOTAL POSTS
    # ====================================
    total = len(posts)

    if total == 0:
        total = 1

    # ====================================
    # POSITIVE %
    # ====================================
    positive_percentage = int(
        (positive / total) * 100
    )

    negative_percentage = int(
        (negative / total) * 100
    )

    neutral_percentage = int(
        (neutral / total) * 100
    )

    # ====================================
    # 🔥 REAL SALES PREDICTION
    # ====================================
    sales_prediction = int(

        (
            positive_percentage * 0.7
        )

        +

        (
            trend_score * 0.3
        )
    )

    # ====================================
    # OVERALL SENTIMENT
    # ====================================
    if positive > negative:

        overall_sentiment = "Positive"

    elif negative > positive:

        overall_sentiment = "Negative"

    else:

        overall_sentiment = "Neutral"

    # ====================================
    # SIMILAR PRODUCTS
    # ====================================
    alternatives = products[
        product
    ]["alternatives"]

    # ====================================
    # BEST COMPETITOR
    # ====================================
    top_competitor = alternatives[0]

    # ====================================
    # AI SUGGESTION
    # ====================================
    if sales_prediction >= 80:

        suggestion = (

            f"{product.title()} currently has "
            f"strong market demand and high "
            f"social engagement."
        )

    elif sales_prediction <= 50:

        suggestion = (

            f"Users are discussing negative "
            f"issues about {product.title()}. "
            f"{top_competitor} currently shows "
            f"better growth."
        )

    else:

        suggestion = (

            f"{product.title()} has stable "
            f"engagement. Marketing improvements "
            f"could increase demand."
        )

    # ====================================
    # RETURN FINAL DATA
    # ====================================
    return {

        "product":
        product.title(),

        "overall_sentiment":
        overall_sentiment,

        "positive_percentage":
        positive_percentage,

        "negative_percentage":
        negative_percentage,

        "neutral_percentage":
        neutral_percentage,

        "trend_score":
        trend_score,

        "sales_prediction":
        sales_prediction,

        "similar_products":
        alternatives,

        "top_competitor":
        top_competitor,

        "ai_suggestion":
        suggestion,

        "live_posts":
        posts[:10]
    }


# ============================================
# 🧪 TEST
# ============================================
if __name__ == "__main__":

    result = analyze_product(
        "iphone 15"
    )

    print(result)
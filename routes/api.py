from flask import Blueprint, jsonify, request, send_file
from src.data_sources import get_tweets
from services.ml_service import predict_one
from services.trend_service import get_trends, get_insight

import random

api = Blueprint("api", __name__)

# ======================================
# LIVE DATA
# ======================================

@api.route("/live-data")
def live_data():

    tweets = get_tweets("product")

    preds = [predict_one(tweet) for tweet in tweets]

    pos = list(preds).count("Positive")
    neg = list(preds).count("Negative")
    neu = list(preds).count("Neutral")

    return jsonify({
        "positive": pos,
        "negative": neg,
        "neutral": neu,
        "tweets": tweets[:5],
        "trends": get_trends(tweets),
        "insight": get_insight(pos, neg)
    })


# ======================================
# SENTIMENT ANALYZE
# ======================================

@api.route("/sentiment/analyze", methods=["POST"])
def analyze_sentiment():

    data = request.get_json()

    text = data.get("text", "")

    sentiment = random.choice([
        "Positive",
        "Negative",
        "Neutral"
    ])

    emotion = random.choice([
        "Happy",
        "Excited",
        "Angry",
        "Neutral"
    ])

    return jsonify({

        "sentiment": sentiment,

        "emotion": emotion,

        "insight":
        f"AI detected {sentiment} sentiment.",

        "counts": {

            "total": 100,

            "Positive": 65,

            "Negative": 20,

            "Neutral": 15
        }
    })


# ======================================
# PRODUCT ANALYSIS
# ======================================

@api.route("/sentiment/product", methods=["POST"])
def analyze_product():

    data = request.get_json()

    product = data.get("product", "").strip()

    if not product:
        return jsonify({
            "error": "Product Not Found"
        })

    return jsonify({

        "product": product,

        "overall_sentiment": random.choice([
            "Positive",
            "Neutral",
            "Negative"
        ]),

        "sales_prediction":
        random.randint(70, 99),

        "trend_score":
        random.randint(60, 100),

        "ai_suggestion":
        f"{product} is trending on social media.",

        "top_competitor":
        "Samsung S24 Ultra",

        "similar_products": [

            "iPhone 12",
            "iPhone 13",
            "Samsung S24",
            "Google Pixel 9"
        ],

        "live_posts": [

            {
                "platform": "Twitter X",
                "text":
                f"{product} is awesome 🔥"
            },

            {
                "platform": "Reddit",
                "text":
                f"{product} battery backup is great!"
            }
        ]
    })


# ======================================
# LIVE STREAM
# ======================================

@api.route("/sentiment/stream")
def stream():

    samples = [

        {
            "sentiment": "Positive",
            "text": "People love the new AI phones 🔥",
            "platform": "Twitter X"
        },

        {
            "sentiment": "Negative",
            "text": "Battery issue discussions increasing.",
            "platform": "Reddit"
        },

        {
            "sentiment": "Neutral",
            "text": "New product launches expected soon.",
            "platform": "Instagram"
        }
    ]

    return jsonify(random.choice(samples))


# ======================================
# REPORT
# ======================================

@api.route("/sentiment/report")
def report():

    return jsonify({
        "message":
        "Report downloaded successfully"
    })
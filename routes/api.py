from flask import Blueprint, jsonify
from src.data_sources import get_tweets
from services.ml_service import predict
from services.trend_service import get_trends, get_insight

api = Blueprint("api", __name__)

@api.route("/live-data")
def live_data():

    tweets = get_tweets("product")

    preds = predict(tweets)

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
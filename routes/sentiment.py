# ============================================
# 🚀 sentiment.py
# ============================================

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

from vaderSentiment.vaderSentiment import (
    SentimentIntensityAnalyzer
)

from database.db import (
    get_history,
    save_prediction
)

from collections import Counter
from datetime import datetime
import random

# PDF
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import (
    getSampleStyleSheet
)

# 🔥 PRODUCT ENGINE
from product_engine import analyze_product

router = APIRouter()

# ============================================
# 🧠 AI MODEL
# ============================================
analyzer = SentimentIntensityAnalyzer()


# ============================================
# 🔍 SENTIMENT ANALYSIS
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
# 😃 EMOTION DETECTION
# ============================================
def detect_emotion(score):

    if score >= 0.6:

        return "Happy"

    elif score <= -0.6:

        return "Angry"

    elif score < 0:

        return "Sad"

    else:

        return "Neutral"


# ============================================
# 🤖 AI INSIGHT
# ============================================
def generate_insight(stats):

    if stats["Positive"] > stats["Negative"]:

        return (
            "🔥 Positive sentiment is increasing"
        )

    elif stats["Negative"] > stats["Positive"]:

        return (
            "⚠ Negative sentiment is increasing"
        )

    else:

        return (
            "😐 Sentiment is balanced"
        )


# ============================================
# 🚀 ANALYZE TEXT
# ============================================
@router.post("/analyze")
def analyze(data: dict):

    try:

        text = data.get(
            "text",
            ""
        ).strip()

        if not text:

            raise HTTPException(
                status_code=400,
                detail="No text provided"
            )

        # sentiment
        sentiment, score = analyze_sentiment(
            text
        )

        confidence = abs(score)

        emotion = detect_emotion(score)

        # save database
        try:

            save_prediction(
                text,
                sentiment,
                confidence,
                datetime.now()
            )

        except Exception as e:

            print("DB ERROR:", e)

        stats = get_stats()

        insight = generate_insight(stats)

        return {

            "text":
            text,

            "sentiment":
            sentiment,

            "emotion":
            emotion,

            "confidence":
            confidence,

            "counts":
            stats,

            "insight":
            insight
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# ============================================
# 📊 STATS
# ============================================
@router.get("/stats")
def get_stats():

    try:

        data = get_history()

        stats = {

            "Positive": 0,
            "Negative": 0,
            "Neutral": 0,
            "total": len(data)
        }

        for row in data:

            s = row.get(
                "sentiment",
                "Neutral"
            )

            if s in stats:

                stats[s] += 1

        return stats

    except Exception as e:

        print("STATS ERROR:", e)

        return {

            "Positive": 0,
            "Negative": 0,
            "Neutral": 0,
            "total": 0
        }


# ============================================
# 📡 LIVE FEED
# ============================================
@router.get("/live")
def live():

    try:

        data = get_history()

        return data[::-1] if data else []

    except Exception as e:

        print("LIVE ERROR:", e)

        return []


# ============================================
# 📊 TREND GRAPH
# ============================================
@router.get("/trend")
def trend():

    try:

        data = get_history()

        return [

            {
                "time":
                str(
                    row.get(
                        "timestamp",
                        ""
                    )
                )[11:19],

                "sentiment":
                row.get(
                    "sentiment",
                    "Neutral"
                )
            }

            for row in data[-15:]
        ]

    except Exception as e:

        print("TREND ERROR:", e)

        return []


# ============================================
# 🔑 KEYWORDS
# ============================================
@router.get("/keywords")
def keywords():

    try:

        data = get_history()

        words = []

        for d in data:

            words += d.get(
                "text",
                ""
            ).lower().split()

        common = Counter(words).most_common(10)

        return [

            {
                "word": w,
                "count": c
            }

            for w, c in common
        ]

    except Exception as e:

        print("KEYWORD ERROR:", e)

        return []


# ============================================
# 📄 PDF REPORT
# ============================================
@router.get("/report")
def report():

    try:

        stats = get_stats()

        filename = "sentiment_report.pdf"

        doc = SimpleDocTemplate(
            filename
        )

        styles = getSampleStyleSheet()

        content = [

            Paragraph(
                "AI Sentiment Report",
                styles["Title"]
            ),

            Spacer(1, 15),

            Paragraph(
                f"Generated on: {datetime.now()}",
                styles["Normal"]
            ),

            Spacer(1, 15),

            Paragraph(
                f"Total Posts: {stats['total']}",
                styles["Normal"]
            ),

            Paragraph(
                f"Positive: {stats['Positive']}",
                styles["Normal"]
            ),

            Paragraph(
                f"Negative: {stats['Negative']}",
                styles["Normal"]
            ),

            Paragraph(
                f"Neutral: {stats['Neutral']}",
                styles["Normal"]
            )
        ]

        doc.build(content)

        return FileResponse(
            path=filename,
            filename=filename,
            media_type="application/pdf"
        )

    except Exception as e:

        return {
            "error": str(e)
        }


# ============================================
# 📡 LIVE SOCIAL STREAM
# ============================================
@router.get("/stream")
def stream():

    posts = [

        {
            "platform": "X",
            "text": "AI technology is the future"
        },

        {
            "platform": "Instagram",
            "text": "This product is amazing!"
        },

        {
            "platform": "Facebook",
            "text": "Service quality is terrible"
        },

        {
            "platform": "YouTube",
            "text": "Excellent customer support"
        },

        {
            "platform": "Reddit",
            "text": "Delivery was too slow"
        },

        {
            "platform": "LinkedIn",
            "text": "This startup will grow fast"
        }
    ]

    post = random.choice(posts)

    sentiment, score = analyze_sentiment(
        post["text"]
    )

    return {

        "platform":
        post["platform"],

        "text":
        post["text"],

        "sentiment":
        sentiment,

        "confidence":
        abs(score)
    }


# ============================================
# 🛒 PRODUCT ANALYSIS API
# ============================================
@router.post("/product")
def product(data: dict):

    name = data.get(
        "product",
        ""
    )

    return analyze_product(name)
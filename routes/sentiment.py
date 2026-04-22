from fastapi import APIRouter, HTTPException
from src.analysis_tools import SentimentAnalyzer

# =============================
# 🔹 INIT ROUTER (MUST BE FIRST)
# =============================
router = APIRouter()

# =============================
# 🔹 INIT ANALYZER
# =============================
analyzer = SentimentAnalyzer()

# =============================
# 🔹 MEMORY STATS
# =============================
stats = {
    "Positive": 0,
    "Negative": 0,
    "Neutral": 0,
    "total": 0
}

# =============================
# 🔹 ANALYZE ROUTE
# =============================
@router.post("/analyze")
def analyze(data: dict):

    print("🔥 API HIT")

    text = data.get("text", "").strip()

    if not text:
        raise HTTPException(status_code=400, detail="No text provided")

    # 🔥 GET RESULT (DICT)
    result = analyzer.predict_sentiment(text)

    sentiment = result["sentiment"]
    confidence = result["confidence"]

    print("🧠 RESULT:", result)

    # =============================
    # 🔥 UPDATE STATS
    # =============================
    stats[sentiment] += 1
    stats["total"] += 1

    return {
        "text": text,
        "sentiment": sentiment,
        "confidence": confidence,
        "counts": stats,
        "total": stats["total"]
    }

# =============================
# 🔹 GET STATS
# =============================
@router.get("/stats")
def get_stats():
    return stats

# =============================
# 🔹 RESET STATS
# =============================
@router.post("/reset")
def reset_stats():
    global stats
    stats = {
        "Positive": 0,
        "Negative": 0,
        "Neutral": 0,
        "total": 0
    }
    return {"message": "Stats reset successfully"}
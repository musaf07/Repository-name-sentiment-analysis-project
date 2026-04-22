from collections import Counter

def get_trends(texts):
    words = " ".join(texts).split()
    return [w for w, _ in Counter(words).most_common(5)]


def get_insight(pos, neg):
    if pos > neg:
        return "📈 Positive sentiment dominating"
    elif neg > pos:
        return "⚠️ Negative sentiment increasing"
    else:
        return "😐 Neutral sentiment stable"
import sqlite3

DB_NAME = "sentiment.db"

# ================= INIT DB =================
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        text TEXT,
        sentiment TEXT,
        confidence REAL
    )
    """)

    conn.commit()
    conn.close()


# ================= SAVE =================
def save_prediction(text, sentiment, confidence):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO history (text, sentiment, confidence) VALUES (?, ?, ?)",
        (text, sentiment, confidence)
    )

    conn.commit()
    conn.close()


# ================= GET =================
def get_history():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("SELECT text, sentiment, confidence FROM history")
    rows = cur.fetchall()

    conn.close()

    return [
        {"text": r[0], "sentiment": r[1], "confidence": r[2]}
        for r in rows
    ]
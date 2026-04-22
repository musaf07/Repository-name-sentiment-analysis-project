import sqlite3

DB_NAME = "data.db"


# =============================
# 🔹 CONNECT DATABASE
# =============================
def get_connection():
    return sqlite3.connect(DB_NAME)


# =============================
# 🔹 INITIALIZE DATABASE
# =============================
def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL,
            sentiment TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()
    print("✅ Database initialized")


# =============================
# 🔹 SAVE PREDICTION
# =============================
def save_prediction(text: str, sentiment: str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO predictions (text, sentiment) VALUES (?, ?)",
        (text, sentiment)
    )

    conn.commit()
    conn.close()


# =============================
# 🔹 GET HISTORY
# =============================
def get_history(limit: int = 10):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, text, sentiment FROM predictions ORDER BY id DESC LIMIT ?",
        (limit,)
    )

    data = cursor.fetchall()

    conn.close()
    return data
import pandas as pd
import joblib
import re

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

# =============================
# 🔹 LOAD DATA
# =============================
df = pd.read_csv("dataset_large.csv")

print("📊 Dataset size:", len(df))

# =============================
# 🔹 CLEAN TEXT
# =============================
def clean_text(text):
    text = str(text).lower()
    text = re.sub(r'[^a-z\s]', '', text)
    return text.strip()

df["text"] = df["text"].apply(clean_text)

# =============================
# 🔹 REMOVE EMPTY ROWS
# =============================
df = df[df["text"] != ""]

# =============================
# 🔹 FIX LABELS
# =============================
df["sentiment"] = df["sentiment"].astype(str).str.strip().str.capitalize()

label_map = {
    "Negative": 0,
    "Neutral": 1,
    "Positive": 2
}

df["sentiment"] = df["sentiment"].map(label_map)

# 🔥 CHECK INVALID LABELS
if df["sentiment"].isnull().any():
    print("❌ Invalid labels found:")
    print(df[df["sentiment"].isnull()])
    raise Exception("Fix dataset labels before training")

# =============================
# 🔹 SHUFFLE DATA
# =============================
df = df.sample(frac=1, random_state=42)

# =============================
# 🔹 SPLIT DATA
# =============================
X_train, X_test, y_train, y_test = train_test_split(
    df["text"],
    df["sentiment"],
    test_size=0.2,
    random_state=42,
    stratify=df["sentiment"]
)

# =============================
# 🔹 VECTORIZER
# =============================
vectorizer = TfidfVectorizer(
    stop_words="english",
    ngram_range=(1, 2),   # 🔥 handles "not good"
    max_features=5000
)

X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

# =============================
# 🔹 MODEL (OPTIMIZED)
# =============================
model = LogisticRegression(
    max_iter=3000,          # 🔥 better convergence
    C=2,                    # 🔥 stronger learning
    class_weight="balanced"
)

model.fit(X_train_vec, y_train)

# =============================
# 🔹 EVALUATION
# =============================
y_pred = model.predict(X_test_vec)

accuracy = accuracy_score(y_test, y_pred)

print(f"\n✅ Accuracy: {accuracy * 100:.2f}%")

print("\n📊 Classification Report:")
print(classification_report(y_test, y_pred))

# =============================
# 🔹 SAVE MODEL
# =============================
joblib.dump(model, "model.pkl")
joblib.dump(vectorizer, "vectorizer.pkl")

print("\n💾 Model + Vectorizer saved successfully")
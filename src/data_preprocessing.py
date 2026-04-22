import pandas as pd
import re

# =============================
# 🔹 CLEAN TEXT FUNCTION
# =============================
def clean_text(text):
    text = str(text).lower()

    # 🔥 Remove URLs
    text = re.sub(r"http\S+|www\S+", "", text)

    # 🔥 Remove mentions and hashtags symbols (keep words)
    text = re.sub(r"[@#]", "", text)

    # 🔥 Remove special characters (keep letters + space)
    text = re.sub(r"[^a-zA-Z\s]", "", text)

    # 🔥 IMPORTANT: keep negation words (not, no, never)
    # DO NOT remove stopwords here

    # 🔥 Remove extra spaces
    text = re.sub(r"\s+", " ", text).strip()

    return text


# =============================
# 🔹 MAIN PREPROCESS FUNCTION
# =============================
def preprocess_data(df):

    print("🧹 Cleaning data...")

    # =============================
    # 🔹 DETECT TEXT COLUMN
    # =============================
    if "content" in df.columns:
        df["clean_text"] = df["content"]
    elif "text" in df.columns:
        df["clean_text"] = df["text"]
    elif "clean_text" in df.columns:
        pass
    else:
        raise Exception("❌ No text column found (content/text/clean_text)")

    # =============================
    # 🔹 REMOVE NULL TEXT
    # =============================
    df = df.dropna(subset=["clean_text"])

    # =============================
    # 🔹 APPLY CLEANING
    # =============================
    df["clean_text"] = df["clean_text"].apply(clean_text)

    # =============================
    # 🔹 REMOVE EMPTY ROWS
    # =============================
    df = df[df["clean_text"].str.strip() != ""]

    # =============================
    # 🔹 STANDARDIZE LABELS (VERY IMPORTANT)
    # =============================
    if "sentiment" in df.columns:
        df["sentiment"] = df["sentiment"].astype(str).str.lower()

        label_map = {
            "positive": "Positive",
            "pos": "Positive",
            "1": "Positive",

            "negative": "Negative",
            "neg": "Negative",
            "-1": "Negative",

            "neutral": "Neutral",
            "neu": "Neutral",
            "0": "Neutral"
        }

        df["sentiment"] = df["sentiment"].map(label_map)

        # remove invalid labels
        df = df.dropna(subset=["sentiment"])

    # =============================
    # 🔹 OPTIONAL TIMESTAMP
    # =============================
    if "timestamp" in df.columns:
        try:
            df["timestamp"] = pd.to_datetime(df["timestamp"])
            df["hour"] = df["timestamp"].dt.hour
        except:
            print("⚠️ Timestamp format issue, skipping...")

    print("✅ Preprocessing complete")
    print(df.head())

    return df
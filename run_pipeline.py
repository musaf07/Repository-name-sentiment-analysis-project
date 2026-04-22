import os
import pandas as pd
import pickle

from src.data_preprocessing import preprocess_data
from src.analysis_tools import SentimentAnalyzer


def run_system():
    print("🚀 Starting Sentiment Analysis System...")

    # ================= BASE DIRECTORY =================
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    os.chdir(BASE_DIR)

    print("📁 Current Working Directory:", os.getcwd())

    try:
        # ================= LOAD DATA =================
        file_path = os.path.join(BASE_DIR, "data", "raw", "social_media_data.csv")

        print(f"📂 Loading data from: {file_path}")

        if not os.path.exists(file_path):
            raise FileNotFoundError

        df = pd.read_csv(file_path)

        print("✅ Data loaded successfully")
        print(f"📊 Dataset Shape: {df.shape}")

        # ================= PREPROCESS =================
        df = preprocess_data(df)
        print("✅ Data preprocessing completed")

        # ================= DEBUG DATA (VERY IMPORTANT) =================
        print("\n🔍 Checking sample data:")
        print(df[["clean_text", "sentiment"]].head(10))

        print("\n📊 Sentiment distribution:")
        print(df["sentiment"].value_counts())

        # ================= VALIDATE LABELS =================
        valid_labels = {"Positive", "Negative", "Neutral"}
        df = df[df["sentiment"].isin(valid_labels)]

        if df.empty:
            raise Exception("❌ No valid labeled data after cleaning")

        # ================= TRAIN MODEL =================
        analyzer = SentimentAnalyzer()
        analyzer.train_model(df)
        print("✅ Model trained successfully")

        # ================= SAVE MODEL + VECTORIZER =================
        model_path = os.path.join(BASE_DIR, "model.pkl")
        vectorizer_path = os.path.join(BASE_DIR, "vectorizer.pkl")

        with open(model_path, "wb") as f:
            pickle.dump(analyzer.model, f)

        with open(vectorizer_path, "wb") as f:
            pickle.dump(analyzer.vectorizer, f)

        print("💾 Model saved as model.pkl")
        print("💾 Vectorizer saved as vectorizer.pkl")

        # ================= TEST PREDICTIONS =================
        print("\n💬 Testing AI Predictions:")

        test_cases = [
            "This product is amazing!",
            "This is bad",
            "Worst experience ever",
            "Not good at all",
            "It's okay"
        ]

        for text in test_cases:
            result = analyzer.predict_sentiment(text)
            print(f"Text: {text} → Prediction: {result}")

        print("\n✅ System Completed Successfully")

    except FileNotFoundError:
        print("❌ ERROR: CSV file not found!")
        print(f"👉 Expected path: {file_path}")

    except Exception as e:
        print("❌ ERROR:", str(e))


if __name__ == "__main__":
    run_system()
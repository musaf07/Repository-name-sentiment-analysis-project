import pandas as pd
import random

# =============================
# 🔹 BASE DATA (YOUR DATA)
# =============================
df = pd.read_csv("dataset.csv")

# =============================
# 🔹 SYNONYM REPLACEMENTS
# =============================
synonyms = {
    "good": ["great", "excellent", "awesome"],
    "bad": ["terrible", "awful", "poor"],
    "slow": ["laggy", "sluggish"],
    "fast": ["quick", "speedy"],
    "app": ["application", "software"],
    "product": ["item", "thing"],
    "experience": ["usage", "interaction"]
}

# =============================
# 🔹 AUGMENT TEXT
# =============================
def augment(text):
    words = text.split()
    new_words = []

    for word in words:
        if word in synonyms and random.random() > 0.5:
            new_words.append(random.choice(synonyms[word]))
        else:
            new_words.append(word)

    return " ".join(new_words)

# =============================
# 🔹 GENERATE MORE DATA
# =============================
augmented_data = []

for _ in range(8):  # 🔥 increase multiplier → ~500 rows
    for _, row in df.iterrows():
        new_text = augment(row["text"])
        augmented_data.append({
            "text": new_text,
            "sentiment": row["sentiment"]
        })

# =============================
# 🔹 COMBINE ORIGINAL + NEW
# =============================
df_aug = pd.DataFrame(augmented_data)

final_df = pd.concat([df, df_aug], ignore_index=True)

# =============================
# 🔹 SAVE NEW DATASET
# =============================
final_df.to_csv("dataset_large.csv", index=False)

print("✅ Generated dataset_large.csv with size:", len(final_df))
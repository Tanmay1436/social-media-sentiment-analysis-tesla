# src/clean_text.py
import json, re, os
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

# Download NLTK resources
nltk.download("punkt", quiet=True)
nltk.download("stopwords", quiet=True)
STOP = set(stopwords.words("english"))

def clean(text):
    text = text.lower()
    text = re.sub(r"http\S+","", text)         # remove URLs
    text = re.sub(r"[^a-z0-9\s]","", text)     # remove punctuation
    tokens = [w for w in word_tokenize(text) if w not in STOP]
    return " ".join(tokens)

# Load raw data
raw = json.load(open("data/raw_reddit_tesla.json","r", encoding="utf-8"))
cleaned = []
for p in raw:
    combined = f"{p['title']} {p['selftext']}"
    cleaned.append({
        "id": p["id"],
        "clean_text": clean(combined)
    })

# Save cleaned data
os.makedirs("data", exist_ok=True)
json.dump(cleaned, open("data/cleaned_reddit_tesla.json","w", encoding="utf-8"),
          ensure_ascii=False, indent=2)

print(f"Cleaned {len(cleaned)} posts → data/cleaned_reddit_tesla.json")

# train.py
import json
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer

# โหลด knowledge_base.json
with open("knowledge_base.json", "r", encoding="utf-8") as f:
    kb = json.load(f)

questions = [item["question"] for item in kb]
answers = [item["answer"] for item in kb]

# TF-IDF Vectorizer
vectorizer = TfidfVectorizer(lowercase=True)
X = vectorizer.fit_transform(questions)

# บันทึก Vectorizer + Answers
joblib.dump(vectorizer, "vectorizer.pkl")
joblib.dump(answers, "answers.pkl")

print("Training complete! vectorizer.pkl และ answers.pkl ถูกสร้างแล้ว")

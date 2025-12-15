from sentence_transformers import SentenceTransformer
import joblib
import json

# โหลด knowledge base
with open("knowledge_base.json", "r", encoding="utf-8") as f:
    kb = json.load(f)

questions = [item["question"] for item in kb]
answers = [item["answer"] for item in kb]

# โหลดโมเดล embedding
model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2') # รองรับภาษาไทย

# สร้าง embeddings


question_embeddings = model.encode(questions, convert_to_tensor=True)

# เซฟ embeddings + answers
joblib.dump(question_embeddings, "question_embeddings.pkl")
joblib.dump(answers, "answers.pkl")
print("Embeddings saved!")

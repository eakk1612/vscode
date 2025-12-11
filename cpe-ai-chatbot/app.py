# app.py
from flask import Flask, request, jsonify, send_from_directory, Response
from flask_cors import CORS
import joblib, time, json, os
from rule_based_db import check_rule_based
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__, static_folder='.')
CORS(app)

# ------------------ โหลด Embedding + Answers ------------------
model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')
question_embeddings = joblib.load("question_embeddings.pkl")  # จาก train_embeddings.py
answers = joblib.load("answers.pkl")                          # จาก train_embeddings.py

# ------------------ Hybrid Chatbot ------------------
def hybrid_chatbot(messages):
    # หา latest user message
    last_user = ""
    for m in reversed(messages):
        if m.get("role") == "user":
            last_user = m.get("content", "")
            break
    if not last_user:
        last_user = messages[-1].get("content", "") if messages else ""

    # -------- Rule-based ก่อน --------
    rule_answer = check_rule_based(last_user)
    if rule_answer:
        return rule_answer

    # -------- Embedding + Cosine Similarity --------
    user_emb = model.encode([last_user])
    sim = cosine_similarity(user_emb, question_embeddings)
    best_idx = sim.argmax()
    best_score = sim[0, best_idx]

    # threshold ถ้า similarity ต่ำมาก
    if best_score < 0.5:
        return "ขอโทษครับ ผมยังไม่รู้คำตอบนี้"

    return answers[best_idx]

# --------------------- Endpoints ---------------------
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(force=True)
    messages = data.get("messages", [])
    reply = hybrid_chatbot(messages)
    return jsonify({"reply": reply})

@app.route("/chat_stream", methods=["POST"])
def chat_stream():
    data = request.get_json(force=True)
    messages = data.get("messages", [])
    reply = hybrid_chatbot(messages)

    def generate():
        for char in reply:
            yield f"data: {json.dumps(char)}\n\n"
            time.sleep(0.02)
        yield "event: done\ndata: [DONE]\n\n"

    return Response(generate(), mimetype="text/event-stream")

# Serve UI
@app.route("/ui")
def ui():
    return send_from_directory(".", "index.html")

@app.route("/")
def home():
    return "AI Chatbot backend is running!"

# Serve images folder
@app.route('/images/<path:filename>')
def images(filename):
    return send_from_directory('images', filename)

# --------------------- Run Server ---------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # ใช้ PORT ของ Render หรือ default 5000
    app.run(host="0.0.0.0", port=port, threaded=True)

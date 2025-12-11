from flask import Flask, request, jsonify, send_from_directory, Response
from flask_cors import CORS
from flask import send_from_directory
import joblib
import time
import json

app = Flask(__name__, static_folder='.')
CORS(app)

# โหลดโมเดลที่เทรนไว้ (จาก train.py ของคุณ)
model = joblib.load("model.pkl")
vectorizer = joblib.load("vectorizer.pkl")

def predict_reply_from_messages(messages):
    """
    messages: list of {role: "user"|"assistant", content: "..."}
    สำหรับโมเดลง่ายๆ ที่เราทำ: ใช้ข้อความล่าสุดของผู้ใช้เป็น input
    """
    # หา latest user message
    last_user = ""
    for m in reversed(messages):
        if m.get("role") == "user":
            last_user = m.get("content", "")
            break
    if not last_user:
        last_user = messages[-1].get("content", "") if messages else ""
    X = vectorizer.transform([last_user])
    reply = model.predict(X)[0]
    return reply

# Non-streaming (returns full reply)
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(force=True)
    messages = data.get("messages", [])  # multi-turn: send array of messages
    reply = predict_reply_from_messages(messages)
    return jsonify({"reply": reply})

# Streaming endpoint using Server-Sent Events (SSE)
@app.route("/chat_stream", methods=["POST"])
def chat_stream():
    data = request.get_json(force=True)
    messages = data.get("messages", [])
    reply = predict_reply_from_messages(messages)

    def generate():
        # stream reply character-by-character (simulate real streaming)
        for i in range(len(reply)):
            chunk = reply[i]
            # SSE event: send data lines then blank line
            yield f"data: {json.dumps(chunk)}\n\n"
            time.sleep(0.02)  # ปรับความเร็วได้
        # send done event
        yield "event: done\ndata: [DONE]\n\n"

    return Response(generate(), mimetype="text/event-stream")

# Serve UI via /ui
@app.route("/ui")
def ui():
    return send_from_directory(".", "index.html")

@app.route("/")
def home():
    return "AI Chatbot backend is running!"

@app.route('/images/<path:filename>')
def images(filename):
    return send_from_directory('images', filename)

if __name__ == "__main__":
    app.run(debug=True, threaded=True)

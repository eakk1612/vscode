import os
import json
import time
import google.generativeai as genai
from flask import Flask, request, jsonify, send_from_directory, Response
from flask_cors import CORS

app = Flask(__name__, static_folder='.')
CORS(app)

# =====================================================
# 1. ตั้งค่า API Key
# =====================================================
# ใส่ API Key ของคุณตรงนี้
GOOGLE_API_KEY = "AIzaSyAmP4k-n4X5Xkgf_pXf3RhenNKYS5sl1WA" 
genai.configure(api_key=GOOGLE_API_KEY)

# ใช้โมเดลมาตรฐาน
model = genai.GenerativeModel('models/gemini-2.5-flash')

# =====================================================
# 2. โหลดข้อมูลความรู้ (Knowledge Base)
# =====================================================
knowledge_text = ""
try:
    if os.path.exists('knowledge_base.json'):
        with open('knowledge_base.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            # แปลง JSON เป็นข้อความ Prompt
            knowledge_text = "ข้อมูลสำหรับตอบคำถาม (Knowledge Base):\n"
            for item in data:
                knowledge_text += f"คำถาม: {item['question']}\nคำตอบ: {item['answer']}\n---\n"
        print("✅ โหลดข้อมูล Knowledge Base เรียบร้อย")
    else:
        print("⚠️ ไม่พบไฟล์ knowledge_base.json (AI จะตอบด้วยความรู้ทั่วไป)")
except Exception as e:
    print(f"❌ อ่านไฟล์ knowledge_base.json ไม่ได้: {e}")

# =====================================================
# 3. ฟังก์ชันคุยกับ AI (แก้ไขบั๊กแล้ว)
# =====================================================
def get_gemini_response(messages, stream=False):
    # ดึงข้อความล่าสุด
    last_user_msg = ""
    for m in reversed(messages):
        if m.get("role") == "user":
            last_user_msg = m.get("content", "")
            break
    
    if not last_user_msg: return "..."

    # สร้าง Prompt
    final_prompt = f"""
    คุณคือ AI Chatbot ประจำภาควิชาวิศวกรรมคอมพิวเตอร์ (CPE)
    ให้ตอบคำถามโดยอ้างอิงจากข้อมูลด้านล่างนี้เป็นหลัก:
    
    {knowledge_text}

    คำถามของผู้ใช้: {last_user_msg}
    
    ข้อควรระวัง: 
    - ถ้าข้อมูลมีใน Knowledge Base ให้ตอบตามนั้น
    - ถ้าไม่มีข้อมูล ให้ตอบว่า "ขออภัย ผมไม่มีข้อมูลเกี่ยวกับเรื่องนี้ครับ" หรือตอบตามความรู้ทั่วไปถ้าเป็นเรื่องพื้นฐาน
    """

    try:
        if stream:
            return model.generate_content(final_prompt, stream=True)
        else:
            response = model.generate_content(final_prompt)
            return response.text
    except Exception as e:
        # ส่งคืนเป็นข้อความ Error เพื่อให้ฟังก์ชันอื่นรู้
        return f"Error from AI: {str(e)}"

# =====================================================
# 4. Endpoints
# =====================================================
@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json(force=True)
        messages = data.get("messages", [])
        reply = get_gemini_response(messages, stream=False)
        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"reply": f"System Error: {str(e)}"})

@app.route("/chat_stream", methods=["POST"])
def chat_stream():
    data = request.get_json(force=True)
    messages = data.get("messages", [])

    def generate():
        # เรียก AI
        response_stream = get_gemini_response(messages, stream=True)

        # [แก้บั๊กตรงนี้] เช็คว่าสิ่งที่ได้มาเป็น Error String หรือไม่?
        if isinstance(response_stream, str):
            # ถ้าเป็น Error (string) ให้ส่งกลับไปเลย
            yield f"data: {json.dumps(response_stream)}\n\n"
            yield "event: done\ndata: [DONE]\n\n"
            return

        # ถ้าไม่ใช่ Error แปลว่าเป็น Object ของ Gemini ให้วนลูปอ่าน
        try:
            for chunk in response_stream:
                # เช็คว่ามีข้อความจริงๆ ไหม
                if hasattr(chunk, 'text') and chunk.text:
                    yield f"data: {json.dumps(chunk.text)}\n\n"
            yield "event: done\ndata: [DONE]\n\n"
        except Exception as e:
            # ดักจับ Error ตอนกำลัง Stream
            error_msg = json.dumps(f"Stream Error: {str(e)}")
            yield f"data: {error_msg}\n\n"
            yield "event: done\ndata: [DONE]\n\n"

    return Response(generate(), mimetype="text/event-stream")

@app.route("/ui")
def ui():
    return send_from_directory(".", "index.html")

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('.', filename)

@app.route("/")
def home():
    return "CPE Chatbot (Fixed) is Ready!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
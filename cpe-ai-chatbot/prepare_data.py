import requests # ⚠️ อย่าลืมพิมพ์: pip install requests ใน Terminal ก่อนนะ
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

app = Flask(__name__, static_folder='.')
CORS(app)

# ========================================================
# 🟢 ใส่ Link ที่ได้จาก Google Colab ตรงนี้ (สำคัญมาก!)
# ========================================================
# ตัวอย่าง: "https://a1b2-34-123.ngrok-free.app" (ไม่ต้องมี /chat ต่อท้ายตรงนี้)
COLAB_API_URL = "https://unhideous-subessentially-geoffrey.ngrok-free.dev" 

def get_ai_response(messages):
    last_user_msg = messages[-1].get("content", "")
    
    try:
        print(f"กำลังส่งข้อความไป Colab: {last_user_msg}")
        # ยิงคำถามไปที่ Colab
        payload = {"message": last_user_msg}
        response = requests.post(f"{COLAB_API_URL}/chat", json=payload)
        
        if response.status_code == 200:
            ai_reply = response.json().get("reply", "เกิดข้อผิดพลาดในการดึงข้อมูล")
            print(f"Colab ตอบกลับมาว่า: {ai_reply}")
            return ai_reply
        else:
            return f"Error connecting to Colab: {response.status_code}"
            
    except Exception as e:
        print(f"Connection Error: {e}")
        return f"เชื่อมต่อ Colab ไม่ได้ (เช็คว่ารัน Colab หรือยัง? หรือ Link ผิดไหม?): {str(e)}"

# รับค่าจากหน้าเว็บ
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(force=True)
    messages = data.get("messages", [])
    reply = get_ai_response(messages)
    return jsonify({"reply": reply})

# 🟢 เปิดหน้าเว็บ index.html อัตโนมัติเมื่อเข้า localhost:5000
@app.route("/")
def home():
    return send_from_directory('.', 'index.html')

# โหลดไฟล์รูปภาพ/CSS/JS (ถ้ามี)
@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('.', filename)

if __name__ == "__main__":
    print("🚀 Server เริ่มทำงานแล้ว! เปิด Browser ไปที่ http://127.0.0.1:5000")
    app.run(host="0.0.0.0", port=5000, debug=True)
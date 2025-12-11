from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import joblib

# -----------------------------
# 1) เตรียมชุดข้อมูล (Training Data)
# -----------------------------

questions = [
    "ui คืออะไร",
    "เรียน ui ยากไหม",
    "ออกแบบ ui ทำยังไง",
    "หน้าที่ ui designer คืออะไร",
    "usability คืออะไร",
    "สีแบบไหนเหมาะกับ ui",
]

answers = [
    "UI คือ User Interface คือการออกแบบหน้าตาและปุ่มต่างๆเพื่อให้ผู้ใช้โต้ตอบระบบได้ง่าย",
    "เรียน UI ไม่ยาก แต่ต้องฝึกเรื่องสี ตัวอักษร และการจัด Layout",
    "การออกแบบ UI เริ่มจากการวิเคราะห์ผู้ใช้ เลือกสี ฟอนต์ ปุ่ม และจัด layout",
    "UI Designer มีหน้าที่ออกแบบหน้าตาระบบ ปุ่ม สี ไอคอน การจัดวางต่างๆ",
    "Usability คือความง่ายในการใช้งานของระบบ",
    "สีที่เหมาะกับ UI ต้องมี contrast ที่ดี อ่านง่าย และดึงดูดสายตา",
]

# -----------------------------
# 2) TF-IDF Vectorizer
# -----------------------------
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(questions)

# -----------------------------
# 3) สร้างโมเดล Naive Bayes
# -----------------------------
model = MultinomialNB()
model.fit(X, answers)

# -----------------------------
# 4) เซฟโมเดล
# -----------------------------
joblib.dump(model, "model.pkl")
joblib.dump(vectorizer, "vectorizer.pkl")

print("✔ เทรนเสร็จแล้ว! สร้าง model.pkl และ vectorizer.pkl เรียบร้อย")

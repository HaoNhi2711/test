import sqlite3
import requests

API_KEY = "AIzaSyCrfmV3leDZpJ5z5mo2AwNtMTmmH5ThkU0"
GEMINI_API_URL = "https://gemini.googleapis.com/v1/your_endpoint"

def init_db():
    conn = sqlite3.connect("y_hoc.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS medical_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT UNIQUE,
            answer TEXT
        )
    """)
    conn.commit()
    conn.close()

def query_database(question):
    conn = sqlite3.connect("y_hoc.db")
    cursor = conn.cursor()
    cursor.execute("SELECT answer FROM medical_data WHERE question = ?", (question,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

def send_message_to_gemini(prompt):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }
    data = {
        "prompt": prompt,
        "max_tokens": 100,
        "temperature": 0.7,
    }
    response = requests.post(GEMINI_API_URL, headers=headers, json=data)
    if response.status_code == 200:
        return response.json().get("response", "Xin lỗi, tôi không có câu trả lời cho câu hỏi này.")
    else:
        return "Có lỗi xảy ra khi kết nối với AI."

def insert_sample_data():
    conn = sqlite3.connect("y_hoc.db")
    cursor = conn.cursor()
    sample_data = [
        ("Cảm cúm là gì?", "Cảm cúm là bệnh nhiễm virus gây ra bởi virus influenza."),
        ("Làm sao để phòng tránh sốt xuất huyết?", "Bạn nên diệt muỗi, dọn dẹp nơi trú ẩn của muỗi và ngủ màn."),
    ]
    cursor.executemany("INSERT OR IGNORE INTO medical_data (question, answer) VALUES (?, ?)", sample_data)
    conn.commit()
    conn.close()

def main():
    init_db()
    insert_sample_data()
    print("Gõ 'exit' để thoát.")
    while True:
        question = input("Bạn: ").strip()
        if question.lower() == "exit":
            break
        answer = query_database(question)
        if not answer:
            answer = send_message_to_gemini(question)
        print(f"Bot: {answer}")

if __name__ == "__main__":
    main()
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sqlite3
from typing import List, Optional

app = FastAPI()

# Дозволяємо запити з будь-яких джерел (CORS для Mini App)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- БАЗА ДАНИХ ---
def get_db():
    conn = sqlite3.connect("class11a.db")
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

def init_db():
    conn = sqlite3.connect("class11a.db")
    cursor = conn.cursor()
    
    # Таблиця користувачів
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            role TEXT DEFAULT 'student', -- 'student' або 'teacher'
            pin TEXT NOT NULL
        )
    ''')
    
    # Таблиця оцінок
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS grades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            subject TEXT NOT NULL,
            grade INTEGER NOT NULL,
            date TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    
    # Таблиця оголошень
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS announcements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

init_db()

# --- МОДЕЛІ ДАНИХ ---
class UserLogin(BaseModel):
    name: str
    pin: str

class GradeAdd(BaseModel):
    user_id: int
    subject: str
    grade: int

class AnnouncementCreate(BaseModel):
    text: str

# --- API ЕНДПОЇНТИ ---

@app.post("/api/login")
def login(user: UserLogin, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT id, name, role FROM users WHERE name = ? AND pin = ?", (user.name, user.pin))
    row = cursor.fetchone()
    if not row:
        raise HTTPException(status_code=401, detail="Невірне ім'я або PIN-код")
    return dict(row)

@app.get("/api/students")
def get_students(db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT id, name FROM users WHERE role = 'student'")
    return [dict(r) for r in cursor.fetchall()]

@app.get("/api/grades/{user_id}")
def get_user_grades(user_id: int, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT subject, grade, date FROM grades WHERE user_id = ?", (user_id,))
    return [dict(r) for r in cursor.fetchall()]

@app.post("/api/grades")
def add_grade(data: GradeAdd, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO grades (user_id, subject, grade, date) VALUES (?, ?, ?, date('now'))",
        (data.user_id, data.subject, data.grade)
    )
    db.commit()
    return {"status": "ok"}

@app.get("/api/announcements")
def get_announcements(db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT text, created_at FROM announcements ORDER BY id DESC LIMIT 5")
    return [dict(r) for r in cursor.fetchall()]

@app.post("/api/announcements")
def add_announcement(data: AnnouncementCreate, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("INSERT INTO announcements (text) VALUES (?)", (data.text,))
    db.commit()
    return {"status": "ok"}

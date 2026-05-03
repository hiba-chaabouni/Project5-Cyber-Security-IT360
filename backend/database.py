import sqlite3
import numpy as np
import io

DB_PATH = "face_auth.db"

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS faceprints (
            faceprint_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            vector BLOB NOT NULL,
            captured_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS audit_logs (
            log_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            event_type TEXT,
            result TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            ip_address TEXT
        )
    """)

    conn.commit()
    conn.close()

def vector_to_blob(vector):
    buf = io.BytesIO()
    np.save(buf, vector)
    return buf.getvalue()

def blob_to_vector(blob):
    buf = io.BytesIO(blob)
    return np.load(buf)

def insert_user(username):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (username) VALUES (?)", (username,))
    user_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return user_id

def insert_faceprint(user_id, vector):
    conn = get_connection()
    cursor = conn.cursor()
    blob = vector_to_blob(vector)
    cursor.execute("INSERT INTO faceprints (user_id, vector) VALUES (?, ?)", (user_id, blob))
    conn.commit()
    conn.close()

def get_all_faceprints():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT u.username, f.vector
        FROM faceprints f
        JOIN users u ON f.user_id = u.user_id
    """)
    rows = cursor.fetchall()
    conn.close()

    entries = []
    for row in rows:
        entries.append({
            "username": row["username"],
            "vector": blob_to_vector(row["vector"])
        })
    return entries

def log_event(username, event_type, result, ip_address):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO audit_logs (username, event_type, result, ip_address)
        VALUES (?, ?, ?, ?)
    """, (username, event_type, result, ip_address))
    conn.commit()
    conn.close()
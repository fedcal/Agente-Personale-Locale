import sqlite3
from datetime import datetime
from pathlib import Path

DB_PATH = Path("persist/memory.db")
DB_PATH.parent.mkdir(exist_ok=True, parents=True)

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS memory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT,
            timestamp TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_memory(content: str) -> str:
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO memory (content, timestamp) VALUES (?, ?)",
        (content, datetime.now().isoformat())
    )
    conn.commit()
    conn.close()
    return "Informazione salvata."

def load_memory(limit=10) -> str:
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT content FROM memory ORDER BY id DESC LIMIT ?", (limit,))
    data = [row[0] for row in cur.fetchall()]
    conn.close()
    return "\n".join(data) if data else "Nessuna memoria salvata."

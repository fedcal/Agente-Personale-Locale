import sqlite3
from pathlib import Path
from typing import List, Dict


# Absolute path avoids creating multiple DBs when the cwd changes
DB_PATH = Path(__file__).resolve().parent.parent / "data" / "commands.db"


def ensure_db():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS commands (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE,
        description TEXT,
        params TEXT
    )
    """)
    conn.commit()
    conn.close()


def seed_defaults():
    ensure_db()
    defaults = [
        ("/news", "Cerca notizie recenti sul tema indicato", "<tema> testo libero"),
    ]
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    for name, desc, params in defaults:
        c.execute("INSERT OR IGNORE INTO commands (name, description, params) VALUES (?, ?, ?)", (name, desc, params))
    conn.commit()
    conn.close()


def list_commands() -> List[Dict[str, str]]:
    ensure_db()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    rows = c.execute("SELECT name, description, params FROM commands ORDER BY name").fetchall()
    conn.close()
    return [{"name": r[0], "description": r[1], "params": r[2]} for r in rows]

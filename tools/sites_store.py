import sqlite3
from pathlib import Path
from typing import List, Dict, Optional

# Use an absolute path so the same DB is picked up regardless of the working dir
DB_PATH = Path(__file__).resolve().parent.parent / "data" / "commands.db"


def ensure_db():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS sites (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        url TEXT UNIQUE,
        note TEXT
    )
    """)
    conn.commit()
    conn.close()


def add_site(url: str, note: str = "") -> Dict[str, str | int]:
    ensure_db()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
    INSERT INTO sites (url, note)
    VALUES (?, ?)
    ON CONFLICT(url) DO UPDATE SET note = excluded.note
    """, (url, note))
    conn.commit()
    row = c.execute("SELECT id, url, note FROM sites WHERE url = ?", (url,)).fetchone()
    conn.close()
    if not row:
        return {"url": url, "note": note}
    return {"id": row[0], "url": row[1], "note": row[2]}


def list_sites() -> List[Dict[str, str]]:
    ensure_db()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    rows = c.execute("SELECT id, url, note FROM sites ORDER BY id DESC").fetchall()
    conn.close()
    return [{"id": r[0], "url": r[1], "note": r[2]} for r in rows]


def delete_site(site_id: int) -> bool:
    ensure_db()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM sites WHERE id = ?", (site_id,))
    conn.commit()
    deleted = c.rowcount > 0
    conn.close()
    return deleted


def update_site(site_id: int, url: str, note: str = "") -> Optional[Dict[str, str | int]]:
    """
    Aggiorna url/note di un sito. Restituisce il record aggiornato oppure None se non trovato o in caso di conflitto.
    """
    ensure_db()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    try:
        c.execute("""
        UPDATE sites SET url = ?, note = ?
        WHERE id = ?
        """, (url, note, site_id))
        conn.commit()
        if c.rowcount == 0:
            return None
        row = c.execute("SELECT id, url, note FROM sites WHERE id = ?", (site_id,)).fetchone()
        return {"id": row[0], "url": row[1], "note": row[2]} if row else None
    except sqlite3.IntegrityError:
        # Violazione unique su url
        return None
    finally:
        conn.close()

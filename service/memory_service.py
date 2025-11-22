import sqlite3
import time
from pathlib import Path
from typing import List, Dict

from utils.logger import get_logger
from utils.config_manager import load_config
from memory.memory_manager import MemoryManager

log = get_logger(__name__)
cfg = load_config()


class MemoryService:
    """
    Gestione conversazioni utente/assistant + memorie strutturate.
    """

    def __init__(self, db_path: str = None):
        path = db_path or cfg["memory"].get("sqlite_path", "data/memory.db")
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        self.db_path = Path(path)
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self._init_db()
        self.memory_manager = MemoryManager(base_path="data/memory")

    def _init_db(self):
        try:
            cur = self.conn.cursor()
            cur.execute("""
            CREATE TABLE IF NOT EXISTS chat_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at REAL
            )
            """)
            self.conn.commit()
        except sqlite3.DatabaseError:
            # file corrotto: lo resettiamo
            try:
                self.conn.close()
            except Exception:
                pass
            self.db_path.unlink(missing_ok=True)
            self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
            cur = self.conn.cursor()
            cur.execute("""
            CREATE TABLE chat_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at REAL
            )
            """)
            self.conn.commit()

    def add_message(self, role: str, content: str) -> None:
        cur = self.conn.cursor()
        cur.execute(
            "INSERT INTO chat_history (role, content, created_at) VALUES (?, ?, ?)",
            (role, content, time.time()),
        )
        self.conn.commit()
        # aggiorna anche le memorie stratificate
        if role == "user":
            self.memory_manager.add_memory(content, type="auto")

    def history(self, limit: int = 20) -> List[Dict[str, str]]:
        cur = self.conn.cursor()
        cur.execute(
            "SELECT role, content FROM chat_history ORDER BY id DESC LIMIT ?",
            (limit,),
        )
        rows = cur.fetchall()
        return [{"role": r[0], "text": r[1]} for r in rows][::-1]

    def clear(self):
        cur = self.conn.cursor()
        cur.execute("DELETE FROM chat_history")
        self.conn.commit()
        self.memory_manager.clear_short_term()
        log.info("Cronologia chat cancellata")

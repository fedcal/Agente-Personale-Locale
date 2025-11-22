import json
import time
import sqlite3
from pathlib import Path
try:
    from chromadb import Client
    from chromadb.config import Settings
except Exception:
    Client = None
    Settings = None


class MemoryManager:
    """
    Gestisce TUTTI i livelli di memoria dell'agente:
    - short-term (RAM)
    - medium-term (JSON local file)
    - long-term (SQLite)
    - vector memory (ChromaDB)
    """

    def __init__(self, base_path="data/memory"):
        Path(base_path).mkdir(parents=True, exist_ok=True)

        self.base_path = base_path

        # ---------------- SHORT TERM ----------------
        self.short_term = []

        # ---------------- MEDIUM TERM ----------------
        self.medium_path = Path(base_path) / "medium_memory.json"
        if not self.medium_path.exists():
            self.medium_path.write_text("[]")

        # ---------------- LONG TERM (SQLITE) ----------------
        self.db_path = Path(base_path) / "long_term.db"
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self._init_long_term_db()

        # ---------------- VECTOR MEMORY (CHROMA) ----------------
        self.vector_collection = None
        if Client and Settings:
            try:
                self.chroma_client = Client(Settings(chroma_db_impl="duckdb+parquet",
                                                     persist_directory=str(Path(base_path) / "chroma")))
                self.vector_collection = self.chroma_client.get_or_create_collection("memory_vectors")
            except Exception:
                # Config Chroma non compatibile o non inizializzabile: disattiva vector memory
                self.vector_collection = None

    # ---------------- LONG TERM DB SETUP ----------------
    def _init_long_term_db(self):
        cur = self.conn.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS memories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT,
            data TEXT,
            created_at TIMESTAMP
        )""")
        self.conn.commit()

    # ============================================================
    # ⭐ AGGIUNTA MEMORIE (SCELTA AUTOMATICA DEL TIPO)
    # ============================================================
    def add_memory(self, text: str, type="auto"):
        """
        Aggiunge una memoria al livello corretto.
        """
        if type == "auto":
            type = self._classify_memory(text)

        if type == "short":
            self.short_term.append(text)

        elif type == "medium":
            self._add_medium(text)

        elif type == "long":
            self._add_long_term(text)

        elif type == "vector":
            self._add_vector(text)

        return type

    def _classify_memory(self, text: str):
        """
        Logica basic (poi la evolviamo con un modello).
        """
        if len(text) < 60:
            return "short"
        if "preferisco" in text.lower() or "da ora in poi" in text.lower():
            return "long"
        if len(text) > 100:
            return "vector"

        return "medium"

    # ---------------- MEDIUM TERM ----------------
    def _add_medium(self, text):
        data = json.loads(self.medium_path.read_text())
        data.append({"timestamp": time.time(), "text": text})
        self.medium_path.write_text(json.dumps(data, indent=2))

    # ---------------- LONG TERM ----------------
    def _add_long_term(self, text):
        cur = self.conn.cursor()
        cur.execute(
            "INSERT INTO memories (category, data, created_at) VALUES (?, ?, ?)",
            ("general", text, time.time()),
        )
        self.conn.commit()

    # ---------------- VECTOR MEMORY ----------------
    def _add_vector(self, text):
        import uuid
        if self.vector_collection:
            self.vector_collection.add(
                documents=[text],
                ids=[str(uuid.uuid4())]
            )

    # ============================================================
    # RECUPERO MEMORIE RILEVANTI
    # ============================================================
    def get_relevant_memories(self, query, limit=5):
        """
        Recupera memorie da TUTTI i livelli:
        - short
        - medium
        - long
        - vector (RAG)
        """
        results = []

        # ---- short ----
        results.extend(self.short_term[-limit:])

        # ---- medium ----
        medium = json.loads(self.medium_path.read_text())
        results.extend([m["text"] for m in medium][-limit:])

        # ---- long ----
        cur = self.conn.cursor()
        cur.execute("SELECT data FROM memories ORDER BY id DESC LIMIT ?", (limit,))
        results.extend([row[0] for row in cur.fetchall()])

        # ---- vector ----
        if self.vector_collection:
            vector_results = self.vector_collection.query(
                query_texts=[query],
                n_results=limit
            )

            if vector_results and "documents" in vector_results:
                results.extend(vector_results["documents"][0])

        return list(dict.fromkeys(results))  # remove duplicates

    # ============================================================
    # UTILITY
    # ============================================================
    def clear_short_term(self):
        self.short_term = []

    def compress_short_to_medium(self):
        if not self.short_term:
            return

        compressed = "\n".join(self.short_term)
        self._add_medium(compressed)
        self.clear_short_term()

    def save_structured_memory(self, data: dict, category="general"):
        cur = self.conn.cursor()
        cur.execute(
            "INSERT INTO memories (category, data, created_at) VALUES (?, ?, ?)",
            (category, json.dumps(data), time.time()),
        )
        self.conn.commit()

    def search_structured_memory(self, text_query):
        cur = self.conn.cursor()
        cur.execute("SELECT data FROM memories WHERE data LIKE ?", (f"%{text_query}%",))
        return [json.loads(row[0]) for row in cur.fetchall()]

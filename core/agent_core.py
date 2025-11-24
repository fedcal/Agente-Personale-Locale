from typing import Dict, Any, List

from utils.config_manager import load_config
from utils.logger import get_logger
from service.ollama_service import OllamaService
from service.memory_service import MemoryService
from service.file_manager import FileManager
from service.system_service import SystemService
from service.news_scraper import NewsScraper
from rag.search import semantic_search

log = get_logger(__name__)
cfg = load_config()


class AgentCore:
    """
    Orchestratore principale: incapsula modelli, memoria e tool locali.
    """

    def __init__(self):
        self.ollama = OllamaService()
        self.memory = MemoryService()
        self.files = FileManager()
        self.system = SystemService()
        self.news = NewsScraper()
        self.default_model = cfg["models"]["reasoning"]

    def chat(self, message: str, model: str = None, temperature: float = 0.7) -> Dict[str, Any]:
        if not message.strip():
            return {"response": "Messaggio vuoto."}

        if message.startswith("/news"):
            query = message.replace("/news", "", 1).strip()
            if not query:
                return {"response": "Usa /news <tema> per cercare notizie."}
            items = self.news.search(query, limit=5)
            formatted = "\n".join([f"- {it['title']} ({it['link']})" for it in items])
            return {"response": f"Notizie su '{query}':\n{formatted}", "model": "news"}

        history = self.memory.history(limit=10)
        relevant = self.memory.memory_manager.get_relevant_memories(message, limit=3)
        prompt = self._build_prompt(message, history, relevant)

        chosen_model = model or self.default_model
        if "embed" in chosen_model:
            log.info("[CHAT] Modello embedding richiesto, uso fallback reasoning")
            chosen_model = self.default_model
        log.info("[CHAT] Modello=%s | Utente='%s'", chosen_model, message[:80])
        try:
            reply = self.ollama.generate(prompt, model=chosen_model, temperature=temperature)
        except Exception as exc:
            log.error("Errore Ollama: %s", exc)
            reply = "Errore nel collegamento a Ollama. Verifica che il servizio sia avviato."

        try:
            self.memory.add_message("user", message)
            self.memory.add_message("assistant", reply)
        except Exception as exc:
            log.warning("[MEMORY] Salvataggio non riuscito: %s", exc)

        return {"response": reply, "model": chosen_model}

    def _build_prompt(self, user_message: str, history: List[Dict[str, str]], memories: List[str]) -> str:
        history_text = "\n".join([f"{m['role']}: {m['text']}" for m in history])
        mem_text = "\n".join(memories)
        return (
            f"Contesto recente:\n{history_text}\n\n"
            f"Memorie rilevanti:\n{mem_text}\n\n"
            f"Utente: {user_message}\n"
            "Rispondi in italiano in modo conciso."
        )

    def search_files(self, query: str):
        return self.files.search(query)

    def system_stats(self):
        return self.system.stats()

    def rag_search(self, query: str):
        return semantic_search(query)

    def models(self) -> List[str]:
        models = self.ollama.list_models()
        return models or [
            cfg["models"]["reasoning"],
            cfg["models"]["code"],
        ]

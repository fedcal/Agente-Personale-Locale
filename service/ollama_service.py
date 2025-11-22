import requests
from typing import Dict, Any, List

from utils.logger import get_logger

log = get_logger(__name__)


class OllamaService:
    """
    Wrapper minimale per l'API HTTP di Ollama.
    """

    def __init__(self, base_url: str = "http://localhost:11434/api"):
        self.base_url = base_url.rstrip("/")

    def generate(self, prompt: str, model: str, temperature: float = 0.7) -> str:
        payload = {"model": model, "prompt": prompt, "temperature": temperature}
        try:
            resp = requests.post(f"{self.base_url}/generate", json=payload, timeout=120)
            resp.raise_for_status()
            data = resp.json()
            return data.get("response") or data.get("text") or resp.text
        except Exception as exc:
            log.error("Errore chiamata Ollama: %s", exc)
            return "Errore nella chiamata al modello locale."

    def list_models(self) -> List[str]:
        try:
            resp = requests.get(f"{self.base_url}/tags", timeout=10)
            resp.raise_for_status()
            data = resp.json()
            models = data.get("models") or []
            if isinstance(models, list):
                return [m.get("name", "") for m in models if m.get("name")]
        except Exception as exc:
            log.warning("Impossibile recuperare i modelli: %s", exc)
        return []

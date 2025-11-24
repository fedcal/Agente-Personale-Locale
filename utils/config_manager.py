import json
import os
from pathlib import Path
from typing import Any, Dict

from dotenv import load_dotenv

from config import CONFIG, MEMORY_CONFIG


def load_config() -> Dict[str, Any]:
    """
    Carica le impostazioni partendo dai default in config.py,
    sovrascrivendole con data/config.json e variabili d'ambiente (.env).
    """
    load_dotenv()
    base_cfg = {**CONFIG, "memory": MEMORY_CONFIG}

    # override da file json
    cfg_path = Path("data/config.json")
    if cfg_path.exists():
        try:
            file_cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
            base_cfg.update(file_cfg)
        except Exception:
            pass  # se non valido, continua con default

    # override da env per le secrets
    secrets = base_cfg.get("secrets", {})
    env_map = {
        "telegram_token": os.getenv("TELEGRAM_TOKEN"),
        "whatsapp_token": os.getenv("WHATSAPP_TOKEN"),
        "gmail_user": os.getenv("GMAIL_USER"),
        "gmail_password": os.getenv("GMAIL_PASSWORD"),
        "notion_token": os.getenv("NOTION_TOKEN"),
        "notion_db_id": os.getenv("NOTION_DB_ID"),
    }
    for k, v in env_map.items():
        if v:
            secrets[k] = v
    base_cfg["secrets"] = secrets
    return base_cfg


def get_secret(key: str) -> str:
    cfg = load_config()
    return cfg.get("secrets", {}).get(key, "")


def ensure_data_dirs() -> None:
    """
    Crea le cartelle di lavoro previste dall'applicazione.
    """
    Path("data").mkdir(exist_ok=True)
    Path("persist").mkdir(exist_ok=True)
    Path("logs").mkdir(exist_ok=True)

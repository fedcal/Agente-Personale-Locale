import json
from pathlib import Path
from typing import Any, Dict

from config import CONFIG, MEMORY_CONFIG


def load_config() -> Dict[str, Any]:
    """
    Carica le impostazioni partendo dai default in config.py e
    sovrascrivendole con quanto presente in data/config.json se esiste.
    """
    base_cfg = {**CONFIG, "memory": MEMORY_CONFIG}
    cfg_path = Path("data/config.json")
    if cfg_path.exists():
        try:
            file_cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
            base_cfg.update(file_cfg)
        except Exception:
            # Se il file è vuoto o non valido continuiamo con i default
            pass
    return base_cfg


def ensure_data_dirs() -> None:
    """
    Crea le cartelle di lavoro previste dall'applicazione.
    """
    Path("data").mkdir(exist_ok=True)
    Path("persist").mkdir(exist_ok=True)
    Path("logs").mkdir(exist_ok=True)

from pathlib import Path
from config import CONFIG

ALLOWED_PATHS = [Path(p).expanduser().resolve() for p in CONFIG["allowed_paths"]]

def is_path_allowed(path_str: str) -> bool:
    path = Path(path_str).expanduser().resolve()
    return any(str(path).startswith(str(p)) for p in ALLOWED_PATHS)

def read_file(path_str: str) -> str:
    path = Path(path_str).expanduser().resolve()
    if not is_path_allowed(str(path)):
        return "Accesso negato a questo percorso."
    if not path.exists():
        return f"Errore: il file '{path}' non esiste."
    return path.read_text(encoding="utf-8")

def write_file(data: str) -> str:
    """Formato atteso: 'path::contenuto'"""
    try:
        path_str, content = data.split("::", 1)
        path = Path(path_str).expanduser().resolve()
        if not is_path_allowed(str(path)):
            return "Accesso negato a questo percorso."
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return f"File '{path}' aggiornato."
    except Exception as e:
        return f"Errore scrittura file: {e}"

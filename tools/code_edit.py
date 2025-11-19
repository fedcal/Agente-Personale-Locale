from pathlib import Path
from tools.file_ops import is_path_allowed

def apply_patch(data: str) -> str:
    """
    Formato:
    path::codice_da_cercare::nuovo_codice
    """
    try:
        path_str, old, new = data.split("::", 2)
        path = Path(path_str).expanduser().resolve()
        if not is_path_allowed(str(path)):
            return "Accesso negato a questo percorso."
        if not path.exists():
            return f"File '{path}' non trovato."
        content = path.read_text(encoding="utf-8")
        if old not in content:
            return "Il codice da sostituire non è stato trovato."
        updated = content.replace(old, new)
        path.write_text(updated, encoding="utf-8")
        return f"Patch applicata a {path}"
    except Exception as e:
        return f"Errore patch: {e}"

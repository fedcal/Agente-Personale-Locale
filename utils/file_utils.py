import fnmatch
from pathlib import Path
from typing import Iterable, List, Tuple

from config import CONFIG

ALLOWED_PATHS = [Path(p).expanduser().resolve() for p in CONFIG.get("allowed_paths", [])]


def _is_allowed(path: Path) -> bool:
    return any(str(path).startswith(str(allowed)) for allowed in ALLOWED_PATHS)


def search_files(query: str, exts: Iterable[str] = None, limit: int = 50) -> List[Path]:
    """
    Cerca file nei percorsi consentiti che contengano la query nel nome.
    """
    exts = [e.lower() for e in (exts or [])]
    results: List[Path] = []
    for root in ALLOWED_PATHS:
        for path in root.rglob("*"):
            if not path.is_file():
                continue
            if exts and path.suffix.lower() not in exts:
                continue
            if query.lower() in path.name.lower():
                results.append(path)
                if len(results) >= limit:
                    return results
    return results


def list_files_by_pattern(pattern: str, limit: int = 200) -> List[Path]:
    """
    Ritorna i file che matchano un pattern glob basato su fnmatch.
    """
    results: List[Path] = []
    for root in ALLOWED_PATHS:
        for path in root.rglob("*"):
            if path.is_file() and fnmatch.fnmatch(path.name, pattern):
                results.append(path)
                if len(results) >= limit:
                    return results
    return results


def read_text_file(path_str: str) -> Tuple[bool, str]:
    path = Path(path_str).expanduser().resolve()
    if not _is_allowed(path):
        return False, "Accesso negato a questo percorso."
    if not path.exists():
        return False, f"File non trovato: {path}"
    try:
        return True, path.read_text(encoding="utf-8")
    except Exception as exc:
        return False, f"Errore lettura file {path}: {exc}"


def write_text_file(path_str: str, content: str) -> Tuple[bool, str]:
    path = Path(path_str).expanduser().resolve()
    if not _is_allowed(path):
        return False, "Accesso negato a questo percorso."
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return True, f"File salvato in {path}"
    except Exception as exc:
        return False, f"Errore scrittura file {path}: {exc}"

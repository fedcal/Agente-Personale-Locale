import os
import shutil
from pathlib import Path
from typing import List, Dict, Any

from utils.file_utils import search_files, read_text_file, write_text_file


class FileManager:
    """
    Ricerca, lettura e semplice organizzazione dei file locali nei percorsi consentiti.
    """

    def search(self, query: str, exts: List[str] = None, limit: int = 50) -> List[Dict[str, Any]]:
        results = []
        for path in search_files(query, exts=exts, limit=limit):
            stat = path.stat()
            results.append({
                "name": path.name,
                "path": str(path),
                "size": stat.st_size,
                "modified": stat.st_mtime,
            })
        return results

    def read(self, path: str) -> Dict[str, Any]:
        ok, content = read_text_file(path)
        return {"ok": ok, "content": content}

    def write(self, path: str, content: str) -> Dict[str, Any]:
        ok, msg = write_text_file(path, content)
        return {"ok": ok, "message": msg}

    def organize(self, source_dir: str) -> Dict[str, Any]:
        """
        Organizza i file in sottocartelle basate sull'estensione (uso locale rapido).
        """
        moved = 0
        src = Path(source_dir).expanduser()
        if not src.exists():
            return {"ok": False, "message": "Cartella non trovata"}
        for path in src.iterdir():
            if not path.is_file():
                continue
            target_dir = src / path.suffix.replace(".", "").upper()
            target_dir.mkdir(exist_ok=True)
            shutil.move(str(path), target_dir / path.name)
            moved += 1
        return {"ok": True, "message": f"Organizzati {moved} file"}

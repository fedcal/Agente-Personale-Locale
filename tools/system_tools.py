import subprocess
import platform
from pathlib import Path
from config import CONFIG

ALLOWED_CMDS = CONFIG["allowed_shell_cmds"]
ALLOWED_PATHS = [Path(p).expanduser().resolve() for p in CONFIG["allowed_paths"]]

def run_shell(cmd: str) -> str:
    if not any(cmd.strip().startswith(a) for a in ALLOWED_CMDS):
        return "Comando non consentito dalla policy di sicurezza."
    try:
        if platform.system() == "Windows":
            return subprocess.getoutput(f"cmd /c {cmd}")
        else:
            return subprocess.getoutput(cmd)
    except Exception as e:
        return f"Errore esecuzione comando: {e}"

def list_dir(path_str: str) -> str:
    path = Path(path_str).expanduser().resolve()
    if not any(str(path).startswith(str(p)) for p in ALLOWED_PATHS):
        return "Accesso negato a questa directory."
    if not path.is_dir():
        return "Percorso non valido."
    return "\n".join([f.name for f in path.iterdir()])

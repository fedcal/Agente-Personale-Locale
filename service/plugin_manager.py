from importlib import import_module
from pathlib import Path
from typing import Dict, Callable


class PluginManager:
    """
    Carica moduli Python da una cartella `plugins` e li espone come callable.
    """

    def __init__(self, plugins_dir: str = "plugins"):
        self.plugins_dir = Path(plugins_dir)
        self.plugins_dir.mkdir(exist_ok=True)
        self._registry: Dict[str, Callable] = {}

    def discover(self):
        for file in self.plugins_dir.glob("*.py"):
            mod_name = file.stem
            module = import_module(f"{self.plugins_dir.name}.{mod_name}")
            if hasattr(module, "run"):
                self._registry[mod_name] = getattr(module, "run")

    def run(self, name: str, *args, **kwargs):
        func = self._registry.get(name)
        if not func:
            raise ValueError(f"Plugin {name} non trovato")
        return func(*args, **kwargs)

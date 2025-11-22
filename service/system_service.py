import platform
import psutil
import shutil
from typing import Dict, Any


class SystemService:
    """
    Restituisce metriche basilari del sistema locale.
    """

    def stats(self) -> Dict[str, Any]:
        vm = psutil.virtual_memory()
        disk = shutil.disk_usage("/")
        return {
            "platform": platform.platform(),
            "cpu_percent": psutil.cpu_percent(interval=0.2),
            "memory": {
                "total": vm.total,
                "available": vm.available,
                "percent": vm.percent,
            },
            "disk": {
                "total": disk.total,
                "used": disk.used,
                "free": disk.free,
            },
        }

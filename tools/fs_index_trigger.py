import subprocess, platform

def run_shell(cmd: str) -> str:
    if platform.system() == "Windows":
        # usa shell cmd
        return subprocess.getoutput(f"cmd /c {cmd}")
    else:
        # Linux / macOS
        return subprocess.getoutput(cmd)
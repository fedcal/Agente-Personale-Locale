import tempfile
import subprocess
from pathlib import Path


class VoiceService:
    """
    Gestione minimale TTS tramite `espeak` (se disponibile) e STT placeholder.
    """

    def tts(self, text: str) -> Path:
        wav = Path(tempfile.gettempdir()) / "ares_tts.wav"
        try:
            subprocess.check_call(["espeak", "-w", str(wav), text])
            return wav
        except Exception:
            return wav

    def stt(self, audio_path: str) -> str:
        # Qui andrebbe integrato whisper/vosk. Per ora placeholder.
        return ""

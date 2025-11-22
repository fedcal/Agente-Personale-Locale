from typing import List, Dict

from service.memory_service import MemoryService


class ContextManager:
    """
    Prepara il contesto da passare al modello combinando history e memorie.
    """

    def __init__(self, memory: MemoryService):
        self.memory = memory

    def build(self, user_message: str, limit: int = 5) -> str:
        history = self.memory.history(limit=limit)
        relevant = self.memory.memory_manager.get_relevant_memories(user_message, limit=limit)
        history_text = "\n".join([f"{m['role']}: {m['text']}" for m in history])
        memories_text = "\n".join(relevant)
        return f"Storia recente:\n{history_text}\n\nMemorie:\n{memories_text}"

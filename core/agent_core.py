from memory.memory_manager import MemoryManager

memory = MemoryManager()

def handle_user_message(message):
    memory.add_memory(message)  # classificazione automatica
    relevant = memory.get_relevant_memories(message)
    return relevant
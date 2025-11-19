from tools.memory import save_memory, load_memory

def tool_save_memory(input: str) -> str:
    save_memory(input)
    return "Ok, ho salvato questa informazione nella memoria."

def tool_load_memory(_: str) -> str:
    return load_memory()

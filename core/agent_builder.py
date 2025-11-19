from langchain_community.chat_models import ChatOllama
from langchain.agents import initialize_agent, Tool
from core.prompt import AGENT_SYSTEM_PROMPT
from config import CONFIG
from tools.file_ops import read_file, write_file
from tools.code_edit import apply_patch
from tools.system_tools import run_shell, list_dir
from tools.memory import save_memory, load_memory

def build_agent():
    reasoning_model = ChatOllama(model=CONFIG["models"]["reasoning"], temperature=0.2)

    tools = [
        Tool(name="read_file", func=read_file, description="Legge il contenuto di un file."),
        Tool(name="write_file", func=write_file, description="Scrive/riscrive un file."),
        Tool(name="apply_patch", func=apply_patch, description="Modifica minima del codice."),
        Tool(name="run_shell", func=run_shell, description="Esegue un comando shell."),
        Tool(name="list_dir", func=list_dir, description="Lista i file in una directory."),
        Tool(name="save_memory", func=save_memory, description="Memorizza un'informazione."),
        Tool(name="load_memory", func=load_memory, description="Carica la memoria.")
    ]

    agent = initialize_agent(
        tools=tools,
        llm=reasoning_model,
        agent="chat-zero-shot-react-description",
        verbose=True
    )
    return agent

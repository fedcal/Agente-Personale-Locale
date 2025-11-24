from core.agent_core import AgentCore


class CommandRouter:
    """
    Router minimale per i comandi da console.
    """

    def __init__(self, agent: AgentCore):
        self.agent = agent

    def dispatch(self, text: str):
        if text.startswith("/files "):
            query = text.replace("/files ", "", 1)
            return {"files": self.agent.search_files(query)}
        if text.startswith("/system"):
            return self.agent.system_stats()
        if text.startswith("/rag "):
            return {"answer": self.agent.rag_search(text.replace("/rag ", "", 1))}
        if text.startswith("/news"):
            return self.agent.chat(text)
        return self.agent.chat(text)

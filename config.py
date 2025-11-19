# config.py
CONFIG = {
    "models": {
        "code": "qwen2.5-coder",      # modello per coding
        "reasoning": "llama3.1",      # modello per reasoning e agent
        "embed": "nomic-embed-text"   # modello per RAG / embeddings
    },
    "allowed_paths": [
        "~/projects",
        "~/Documents/work"
    ],
    "allowed_shell_cmds": [
        "ls", "dir", "git status", "git pull", "python -m pytest"
    ]
}

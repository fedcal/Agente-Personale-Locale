# config.json
CONFIG = {
    "models": {
        "code": "qwen2.5-coder:latest",      # modello per coding
        "reasoning": "llama3.1:latest",      # modello per reasoning e agent
        "embed": "nomic-embed-text:latest"   # modello per RAG / embeddings
    },
    "allowed_paths": [
        "~/projects",
        "~/Documents/work"
    ],
    "allowed_shell_cmds": [
        "ls", "dir", "git status", "git pull", "python -m pytest"
    ]
}

MEMORY_CONFIG = {
    "short_term_limit": 20,
    "sqlite_path": "data/memory.db",
    "file_memory_path": "data/files_memory/",
    "chroma_path": "data/embeddings/",
    "use_notion": True,
    "notion_token": "",
    "notion_database_id": ""
}

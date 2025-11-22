import os
from pathlib import Path
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader

CHROMA_PERSIST_DIR = Path("persist/chroma")
CHROMA_PERSIST_DIR.mkdir(exist_ok=True, parents=True)
EMBED_MODEL = "nomic-embed-text"

def scan_paths(root_paths, exts=None, max_files=100000):
    exts = set(exts or [".py", ".java", ".kt", ".js", ".ts", ".html", ".md", ".txt", ".json", ".xml", ".properties"])
    count = 0
    for root in root_paths:
        for dirpath, dirs, files in os.walk(root):
            for name in files:
                if count >= max_files:
                    return
                p = Path(dirpath) / name
                if p.suffix.lower() in exts:
                    yield str(p)
                    count += 1

def index_files(root_paths, persist_dir=CHROMA_PERSIST_DIR, chunk_size=1500, chunk_overlap=200):
    emb = OllamaEmbeddings(model=EMBED_MODEL)
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    docs = []
    for fp in scan_paths(root_paths):
        try:
            loader = TextLoader(fp, encoding="utf-8")
            d = loader.load()
            for doc in d:
                doc.metadata["source"] = fp
                docs.append(doc)
        except Exception as e:
            print(f"skip {fp} : {e}")

    if not docs:
        print("Nessun documento da indicizzare.")
        return

    split_docs = text_splitter.split_documents(docs)
    vectordb = Chroma(persist_directory=str(persist_dir), embedding=emb)
    vectordb.add_documents(split_docs)
    vectordb.persist()
    print(f"Indicizzati {len(split_docs)} chunk in {persist_dir}")

from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import PromptTemplate

CHROMA_PERSIST_DIR = "persist/chroma"
EMBED_MODEL = "nomic-embed-text"
QA_MODEL = "llama3.1"  # reasoning model

def semantic_search(query: str, k=5):
    emb = OllamaEmbeddings(model=EMBED_MODEL)
    vectordb = Chroma(persist_directory=CHROMA_PERSIST_DIR, embedding=emb)
    docs = vectordb.similarity_search(query, k=k)

    # use a reasoning model to synthesize an answer from the retrieved docs
    from langchain_community.chat_models import ChatOllama
    model = ChatOllama(model=QA_MODEL, temperature=0.2)
    template = """Sei un assistente che risponde facendo riferimento ai documenti forniti.
Domanda: {question}
Documenti: {context}
Risposta sintetica, punti chiave e riferimenti ai file (source)."""
    prompt = PromptTemplate(input_variables=["question","context"], template=template)
    context = "\n\n".join([f"---\nSource: {d.metadata.get('source')}\n{d.page_content}" for d in docs])
    prompt_input = prompt.format(question=query, context=context)

    resp = model.generate([{"role":"user", "content": prompt_input}])
    # model.generate may return structured; simplify:
    try:
        return resp.generations[0][0].text
    except Exception:
        return str(resp)

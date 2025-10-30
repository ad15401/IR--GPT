import os, glob, pathlib, json
from dataclasses import dataclass
from typing import List, Dict, Any

# Embeddings + vector store
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings

# PDF reading
from pypdf import PdfReader

# Ollama Python client
import ollama

@dataclass
class Doc:
    page_content: str
    metadata: Dict[str, Any]

# --- Simple loaders (md/txt/pdf) ---
def load_docs(playbooks_dir: str) -> List[Doc]:
    docs: List[Doc] = []
    for path in glob.glob(os.path.join(playbooks_dir, "**/*"), recursive=True):
        if os.path.isdir(path):
            continue
        ext = pathlib.Path(path).suffix.lower()
        try:
            if ext in [".md", ".txt"]:
                with open(path, "r", encoding="utf-8", errors="ignore") as f:
                    docs.append(Doc(page_content=f.read(), metadata={"source": path}))
            elif ext == ".pdf":
                reader = PdfReader(path)
                text = "\n".join([p.extract_text() or "" for p in reader.pages])
                docs.append(Doc(page_content=text, metadata={"source": path}))
        except Exception as e:
            print(f"[loader] Skipping {path}: {e}")
    return docs

# --- Naive text splitter ---
def split_text(text: str, chunk_size: int = 1200, overlap: int = 200) -> List[str]:
    chunks = []
    start = 0
    n = len(text)
    while start < n:
        end = min(start + chunk_size, n)
        chunks.append(text[start:end])
        start = end - overlap
        if start < 0:
            start = 0
        if start >= n:
            break
        if end == n:
            break
    return chunks

def split_docs(docs: List[Doc], chunk_size=1200, overlap=200) -> List[Doc]:
    out: List[Doc] = []
    for d in docs:
        for c in split_text(d.page_content, chunk_size, overlap):
            out.append(Doc(page_content=c, metadata=d.metadata))
    return out

# --- Build / load Chroma collection ---
def get_collection(playbooks_dir: str, persist_dir: str = ".chroma"):
    os.makedirs(persist_dir, exist_ok=True)
    client = chromadb.PersistentClient(path=persist_dir, settings=Settings(allow_reset=True))
    coll = client.get_or_create_collection(name="irgpt")
    # If empty, index the playbooks
    if coll.count() == 0:
        print("[index] Building vector store from playbooks...")
        model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2", device="cpu")
        docs = split_docs(load_docs(playbooks_dir))
        embeddings = model.encode([d.page_content for d in docs], show_progress_bar=True)
        ids = [f"doc-{i}" for i in range(len(docs))]
        metadatas = [d.metadata for d in docs]
        coll.add(ids=ids, embeddings=embeddings, documents=[d.page_content for d in docs], metadatas=metadatas)
        print(f"[index] Added {len(docs)} chunks.")
    return coll

def retrieve(coll, query: str, k: int = 5):
    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2", device="cpu")
    q_emb = model.encode([query])
    res = coll.query(query_embeddings=q_emb, n_results=k)
    # normalize into a list of docs
    out = []
    for i in range(len(res["documents"][0])):
        out.append({
            "page_content": res["documents"][0][i],
            "metadata": res["metadatas"][0][i]
        })
    return out

def format_context(results: List[Dict[str, Any]]) -> str:
    blocks = []
    for i, r in enumerate(results, 1):
        src = os.path.basename(r["metadata"].get("source", "unknown"))
        blocks.append(f"[{i}] Source: {src}\n{r['page_content']}")
    return "\n\n".join(blocks)

def run_llm(query: str, context: str) -> str:
    model_name = os.environ.get("IRGPT_MODEL", "phi3:mini")
    # Load prompts
    with open(os.path.join(os.path.dirname(__file__), "prompts", "system_ir.md"), "r", encoding="utf-8") as f:
        system_prompt = f.read()
    with open(os.path.join(os.path.dirname(__file__), "prompts", "style_guardrails.md"), "r", encoding="utf-8") as f:
        guardrails = f.read()
    prompt = f"""{system_prompt}

{guardrails}

### CONTEXT
{context}

### USER QUERY
{query}

Return your helpful analysis first, then append the JSON block under '###RESPONSE_JSON###'."""
    resp = ollama.generate(model=model_name, prompt=prompt, options={"temperature": 0.2})
    return resp["response"]

def analyze(query: str, playbooks_dir: str = "../data/playbooks", persist_dir: str = "../.chroma") -> Dict[str, Any]:
    # Resolve relative paths from this file
    base_dir = os.path.dirname(os.path.abspath(__file__))
    pb_dir = os.path.normpath(os.path.join(base_dir, playbooks_dir))
    ps_dir = os.path.normpath(os.path.join(base_dir, persist_dir))

    coll = get_collection(pb_dir, ps_dir)
    results = retrieve(coll, query, k=5)
    context = format_context(results)
    response = run_llm(query, context)
    return {
        "response": response,
        "context_snippets": [r["page_content"][:400] for r in results],
        "sources": [r["metadata"].get("source") for r in results],
    }

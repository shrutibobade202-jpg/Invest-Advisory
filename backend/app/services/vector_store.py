from pathlib import Path
from typing import List, Dict, Any, Tuple
import chromadb
from app.config import CHROMA_DB_PATH, settings
from app.services.embeddings import get_embedding_model

_chroma_client = None


def get_chroma_client():
    global _chroma_client
    if _chroma_client is None:
        db_path = Path(CHROMA_DB_PATH)
        if not db_path.exists():
            # Check fallback locations
            fallbacks = [
                Path("C:/Users/shrut/OneDrive/Documents/Goal-Based-Investment-Advisory/chroma_db"),
                Path("C:/Users/shrut/OneDrive/Documents/Goal-Based-Investment-Advisory/backend/chroma_db"),
                Path("C:/Users/shrut/OneDrive/Documents/chroma_db"),
            ]
            for fb in fallbacks:
                if fb.exists() and any(fb.iterdir()):
                    db_path = fb
                    break
        _chroma_client = chromadb.PersistentClient(path=str(db_path))
    return _chroma_client


def get_target_collection():
    client = get_chroma_client()
    collections = client.list_collections()
    if not collections:
        raise RuntimeError("No collections found in ChromaDB.")

    col_names = [c.name for c in collections]
    # Prefer configured collection, then goalinvest_documents, then langchain, then first available
    preferred = [settings.CHROMA_COLLECTION, "goalinvest_documents", "langchain"]
    for name in preferred:
        if name in col_names:
            col = client.get_collection(name)
            if col.count() > 0:
                return col

    # Fallback to first non-empty
    for c in collections:
        col = client.get_collection(c.name)
        if col.count() > 0:
            return col

    return client.get_collection(collections[0].name)


def search_vector_store(query: str, n_results: int = 4) -> List[Dict[str, Any]]:
    """Search ChromaDB for documents most relevant to the query.
    Uses vector embeddings if model is available, falling back gracefully to keyword retrieval.
    """
    collection = get_target_collection()
    if collection.count() == 0:
        return []

    results = []

    # Try embedding-based semantic retrieval first
    try:
        embeddings = get_embedding_model()
        if embeddings:
            query_vector = embeddings.embed_query(query)
            query_res = collection.query(
                query_embeddings=[query_vector],
                n_results=min(n_results * 2, collection.count()),
                include=["documents", "metadatas", "distances"]
            )
            if query_res and query_res.get("documents") and query_res["documents"][0]:
                docs = query_res["documents"][0]
                metas = query_res["metadatas"][0] if query_res.get("metadatas") else [{}] * len(docs)
                for doc_text, meta in zip(docs, metas):
                    if doc_text and len(doc_text.strip()) > 30:
                        results.append({
                            "content": doc_text.strip(),
                            "metadata": meta or {}
                        })
    except Exception as e:
        print(f"Embedding search notice: {e}, using text index retrieval.")

    # If semantic retrieval yielded nothing or failed, use token-overlap search
    if not results:
        all_data = collection.get(include=["documents", "metadatas"])
        import re
        words = set(re.findall(r"[a-zA-Z0-9]+", query.lower()))
        stop_words = {
            "what", "how", "why", "when", "where", "which",
            "the", "is", "are", "a", "an", "and", "or",
            "to", "for", "of", "in", "on", "i", "me", "my",
            "can", "you", "please", "explain", "tell", "about"
        }
        keywords = words - stop_words

        scored = []
        for doc_text, meta in zip(all_data.get("documents", []), all_data.get("metadatas", [])):
            if not doc_text or len(doc_text.strip()) < 30:
                continue
            doc_words = set(re.findall(r"[a-zA-Z0-9]+", doc_text.lower()))
            score = len(keywords & doc_words)
            if score > 0:
                scored.append((score, doc_text.strip(), meta or {}))

        scored.sort(key=lambda x: x[0], reverse=True)
        for _, text, meta in scored[:n_results * 2]:
            results.append({
                "content": text,
                "metadata": meta
            })

    # Deduplicate results based on source and snippet
    deduped = []
    seen = set()
    for item in results:
        meta = item["metadata"]
        src = meta.get("source_file") or meta.get("source") or "doc"
        page = meta.get("page", 0)
        snippet_key = (str(src), str(page), item["content"][:80])
        if snippet_key not in seen:
            seen.add(snippet_key)
            deduped.append(item)
            if len(deduped) >= n_results:
                break

    return deduped

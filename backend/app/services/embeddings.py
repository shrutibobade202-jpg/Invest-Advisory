from functools import lru_cache
from app.config import settings

_embeddings_instance = None


def get_embedding_model():
    """Lazy load embedding model so server starts instantly."""
    global _embeddings_instance
    if _embeddings_instance is None:
        try:
            from langchain_huggingface import HuggingFaceEmbeddings
            _embeddings_instance = HuggingFaceEmbeddings(
                model_name=settings.EMBEDDING_MODEL
            )
        except Exception as e:
            print(f"Warning: Failed to load HuggingFaceEmbeddings ({e}), attempting fallback...")
            try:
                from langchain_community.embeddings import HuggingFaceEmbeddings as CommunityEmbeddings
                _embeddings_instance = CommunityEmbeddings(
                    model_name=settings.EMBEDDING_MODEL
                )
            except Exception as e2:
                print(f"Embeddings error: {e2}")
                _embeddings_instance = None
    return _embeddings_instance

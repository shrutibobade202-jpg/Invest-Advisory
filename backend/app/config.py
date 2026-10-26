import os
from pathlib import Path
from typing import List
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    APP_ENV: str = "development"
    APP_TITLE: str = "GoalInvest Advisor"
    APP_VERSION: str = "1.0.0"

    # LLM Settings
    LLM_PROVIDER: str = "openai"  # "openai", "ollama", or "fallback"
    OPENAI_API_KEY: str = Field(default="")
    LLM_MODEL: str = "gpt-4o-mini"
    OLLAMA_MODEL: str = "llama3.2:3b"
    OLLAMA_BASE_URL: str = "http://localhost:11434"

    # Embedding & Vector DB Settings
    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"
    CHROMA_COLLECTION: str = "goalinvest_documents"
    CHROMA_DB_PATH: str = ""
    DATA_DIR: str = ""

    # CORS Settings
    FRONTEND_ORIGINS: str = "http://localhost:5173,http://localhost:5174,http://127.0.0.1:5173,http://127.0.0.1:5174,https://shrutibobade202-jpg.github.io"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"

    @property
    def cors_origins(self) -> List[str]:
        return [origin.strip() for origin in self.FRONTEND_ORIGINS.split(",") if origin.strip()]

    def resolve_paths(self):
        """Resolve project paths whether running from backend root, backend/app, or project root."""
        current_file = Path(__file__).resolve()
        # candidate directories for project root
        candidates = [
            current_file.parent.parent.parent,  # Goal-Based-Investment-Advisory
            current_file.parent.parent,         # backend
            Path.cwd(),
            Path.cwd().parent
        ]

        resolved_data_dir = None
        resolved_chroma_dir = None

        if self.DATA_DIR and Path(self.DATA_DIR).is_absolute() and Path(self.DATA_DIR).exists():
            resolved_data_dir = Path(self.DATA_DIR)
        else:
            for cand in candidates:
                # check data or backend/data
                if (cand / "data").exists():
                    resolved_data_dir = cand / "data"
                    break
                elif (cand / "backend" / "data").exists():
                    resolved_data_dir = cand / "backend" / "data"
                    break

        if self.CHROMA_DB_PATH and Path(self.CHROMA_DB_PATH).is_absolute() and Path(self.CHROMA_DB_PATH).exists():
            resolved_chroma_dir = Path(self.CHROMA_DB_PATH)
        else:
            for cand in candidates:
                if (cand / "chroma_db").exists() and any((cand / "chroma_db").iterdir()):
                    resolved_chroma_dir = cand / "chroma_db"
                    break
                elif (cand / "backend" / "chroma_db").exists() and any((cand / "backend" / "chroma_db").iterdir()):
                    resolved_chroma_dir = cand / "backend" / "chroma_db"
                    break

        # Defaults if not found yet
        if not resolved_data_dir:
            resolved_data_dir = current_file.parent.parent.parent / "data"
        if not resolved_chroma_dir:
            resolved_chroma_dir = current_file.parent.parent / "chroma_db"

        return resolved_data_dir, resolved_chroma_dir


settings = Settings()
DATA_DIR, CHROMA_DB_PATH = settings.resolve_paths()

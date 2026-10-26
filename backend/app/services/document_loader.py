import os
from pathlib import Path
from typing import List, Dict, Any
from app.config import DATA_DIR


def get_available_documents() -> List[Dict[str, Any]]:
    """Scan the data directory and list all authentic source documents."""
    data_path = Path(DATA_DIR)
    if not data_path.exists():
        # Fallback to backend/data
        alt = Path(__file__).resolve().parent.parent.parent / "data"
        if alt.exists():
            data_path = alt

    docs = []
    if not data_path.exists():
        return docs

    for file_path in data_path.rglob("*"):
        if not file_path.is_file():
            continue
        # Skip node_modules, temp files, js bundles
        if any(ignored in file_path.parts for ignored in ["node_modules", ".git", "__pycache__", "js.download"]):
            continue
        if file_path.suffix.lower() not in [".pdf", ".md", ".txt", ".csv", ".html"]:
            continue
        if file_path.name.endswith(".js.download"):
            continue

        try:
            rel = file_path.relative_to(data_path)
            source_type = rel.parts[0] if len(rel.parts) > 1 else "general"
        except ValueError:
            source_type = "general"

        docs.append({
            "filename": file_path.name,
            "relative_path": str(rel),
            "source_type": source_type,
            "size_bytes": file_path.stat().st_size,
            "absolute_path": str(file_path),
        })

    return docs

from fastapi import APIRouter, HTTPException
from pathlib import Path
import sqlite3
import os
from geneweb.core.database import BaseManager

router = APIRouter(prefix="/api/bases", tags=["admin:stats"])

KNOWN_TABLES = [
    "persons",
    "families",
    "events",
    "relations",
    "children_in_family",
    "media",
    "notes",
    "sources",
]


def _count_rows(db_path: Path) -> dict:
    counts = {}
    con = sqlite3.connect(db_path)
    try:
        cur = con.cursor()
        for table in KNOWN_TABLES:
            try:
                cur.execute(f"SELECT COUNT(*) FROM {table}")
                result = cur.fetchone()
                counts[table] = result[0] if result and result[0] is not None else 0
            except Exception:
                counts[table] = 0
    finally:
        con.close()
    return counts


@router.get("/{name}/stats")
def get_base_stats(name: str, base_dir: str | None = None):
    base_dir = base_dir or os.getenv("BASES_PATH", "./bases")

    path = BaseManager.base_path(name, base_dir)
    if not path.exists():
        raise HTTPException(status_code=404, detail="Base not found")

    return {
        "name": name,
        "path": str(path),
        "size_bytes": os.path.getsize(path),
        "modified_ts": int(os.path.getmtime(path)),
        "counts": _count_rows(path),
    }

import os, re, sqlite3
from pathlib import Path
from typing import List

VALID = re.compile(r"^[A-Za-z0-9_-]{1,64}$")

def ensure_dir(p: Path) -> None:
    p.mkdir(parents=True, exist_ok=True)

def bases_dir(base_dir: str | Path | None) -> Path:
    return Path(base_dir or "./bases").resolve()

def list_bases(base_dir: str | Path | None = None) -> List[str]:
    d = bases_dir(base_dir)
    ensure_dir(d)
    return sorted(p.stem for p in d.glob("*.db"))

def base_path(name: str, base_dir: str | Path | None = None) -> Path:
    if not VALID.match(name):
        raise ValueError("invalid base name")
    d = bases_dir(base_dir)
    ensure_dir(d)
    return d / f"{name}.db"

def create_base(name: str, base_dir: str | Path | None = None) -> None:
    path = base_path(name, base_dir)
    if path.exists():
        raise FileExistsError("base already exists")
    sqlite3.connect(path).close()

def cleanup_base(name: str, base_dir: str | Path | None = None) -> None:
    path = base_path(name, base_dir)
    if not path.exists():
        raise FileNotFoundError("base not found")
    con = sqlite3.connect(path)
    try:
        con.execute("PRAGMA journal_mode=WAL;")
        con.execute("VACUUM;")
        con.execute("PRAGMA optimize;")
        con.commit()
    finally:
        con.close()

def rename_base(old: str, new: str, base_dir: str | Path | None = None) -> None:
    src = base_path(old, base_dir)
    dst = base_path(new, base_dir)
    if not src.exists():
        raise FileNotFoundError("base not found")
    if dst.exists():
        raise FileExistsError("target already exists")
    os.replace(src, dst)

def delete_base(name: str, base_dir: str | Path | None = None) -> None:
    path = base_path(name, base_dir)
    if not path.exists():
        raise FileNotFoundError("base not found")
    path.unlink()

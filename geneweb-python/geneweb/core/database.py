from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from geneweb.core.models.alchemyBase import Base
from geneweb.core.models.ChildInFamily import ChildInFamily
from geneweb.core.models.Event import Event
from geneweb.core.models.Family import Family
from geneweb.core.models.Media import Media
from geneweb.core.models.Note import Note
from geneweb.core.models.Person import Person
from geneweb.core.models.Relation import Relation
from geneweb.core.models.Source import Source

import os
import re
import sqlite3


class Database:
    BASES_FOLDER = Path(__file__).parent / "bases"

    def __init__(self, base_name: str = None, in_memory: bool = False):
        if in_memory:
            self.engine = create_engine(
                "sqlite:///:memory:", connect_args={"check_same_thread": False}
            )
        else:
            if not base_name:
                raise ValueError(
                    "A base_name must be provided when "
                    "not using in_memory mode."
                )

            self.base_name = base_name
            self.db_path = self.BASES_FOLDER / f"{base_name}.db"
            self.BASES_FOLDER.mkdir(exist_ok=True)

            if self.db_path.exists():
                raise FileExistsError(
                    f"Database '{self.db_path}' already exists.")

            self.engine = create_engine(
                f"sqlite:///{self.db_path}",
                connect_args={
                    "check_same_thread": False})

        Base.metadata.create_all(bind=self.engine)
        self.SessionLocal = sessionmaker(
            bind=self.engine, expire_on_commit=False)
        self.session = self.SessionLocal()

    def close(self):
        self.session.close()

    @classmethod
    def get_existing_bases(cls) -> list[str]:
        cls.BASES_FOLDER.mkdir(exist_ok=True)
        return [f.stem for f in cls.BASES_FOLDER.glob("*.db") if f.is_file()]

    @classmethod
    def is_base_exist(cls, base_name) -> bool:
        return base_name in cls.get_existing_bases()


class BaseManager:
    VALID = re.compile(r"^[A-Za-z0-9_-]{1,64}$")

    @staticmethod
    def bases_dir(base_dir: str | Path | None = None) -> Path:
        d = Path(base_dir or "./bases").resolve()
        d.mkdir(parents=True, exist_ok=True)
        return d

    @classmethod
    def list_bases(cls, base_dir: str | Path | None = None) -> list[str]:
        d = cls.bases_dir(base_dir)
        return sorted(p.stem for p in d.glob("*.db"))

    @classmethod
    def _validate_name(cls, name: str):
        if not cls.VALID.match(name):
            raise ValueError("Invalid base name")

    @classmethod
    def base_path(cls, name: str, base_dir: str | Path | None = None) -> Path:
        cls._validate_name(name)
        return cls.bases_dir(base_dir) / f"{name}.db"

    @classmethod
    def create_base(cls, name: str, base_dir: str | Path | None = None):
        path = cls.base_path(name, base_dir)
        if path.exists():
            raise FileExistsError("Base already exists")
        sqlite3.connect(path).close()

    @classmethod
    def delete_base(cls, name: str, base_dir: str | Path | None = None):
        path = cls.base_path(name, base_dir)
        if not path.exists():
            raise FileNotFoundError("Base not found")
        path.unlink()

    @classmethod
    def rename_base(
            cls,
            old: str,
            new: str,
            base_dir: str | Path | None = None):
        src = cls.base_path(old, base_dir)
        dst = cls.base_path(new, base_dir)
        if not src.exists():
            raise FileNotFoundError("Base not found")
        if dst.exists():
            raise FileExistsError("Target already exists")
        os.replace(src, dst)

    @classmethod
    def cleanup_base(cls, name: str, base_dir: str | Path | None = None):
        path = cls.base_path(name, base_dir)
        if not path.exists():
            raise FileNotFoundError("Base not found")
        con = sqlite3.connect(path)
        try:
            con.execute("PRAGMA journal_mode=WAL;")
            con.execute("VACUUM;")
            con.execute("PRAGMA optimize;")
            con.commit()
        finally:
            con.close()

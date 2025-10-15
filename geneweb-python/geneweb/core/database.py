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

class Database:
    BASES_FOLDER = Path(__file__).parent / "bases"

    def __init__(self, base_name: str = None, in_memory: bool = False):
        if in_memory:
            # Utilise une base SQLite en mémoire (disparaît après le test)
            self.engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
        else:
            if not base_name:
                raise ValueError("A base_name must be provided when not using in_memory mode.")

            self.base_name = base_name
            self.db_path = self.BASES_FOLDER / f"{base_name}.db"
            self.BASES_FOLDER.mkdir(exist_ok=True)

            if self.db_path.exists():
                raise FileExistsError(f"Database '{self.db_path}' already exists.")

            self.engine = create_engine(f"sqlite:///{self.db_path}", connect_args={"check_same_thread": False})

        Base.metadata.create_all(bind=self.engine)
        self.SessionLocal = sessionmaker(bind=self.engine, expire_on_commit=False)
        self.session = self.SessionLocal()

    def close(self):
        self.session.close()
    
    @classmethod
    def get_existing_bases(cls) -> list[str]:
        cls.BASES_FOLDER.mkdir(exist_ok=True)
        return [
            f.stem
            for f in cls.BASES_FOLDER.glob("*.db")
            if f.is_file()
        ]

    @classmethod
    def is_base_exist(cls, base_name) -> bool:
        return base_name in cls.get_existing_bases()

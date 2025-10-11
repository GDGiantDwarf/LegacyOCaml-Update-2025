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
            self.base_name = base_name
            self.db_path = self.BASES_FOLDER / f"{base_name}.db"
            self.BASES_FOLDER.mkdir(exist_ok=True)
            self.engine = create_engine(f"sqlite:///{self.db_path}", connect_args={"check_same_thread": False})

        Base.metadata.create_all(bind=self.engine)
        self.SessionLocal = sessionmaker(bind=self.engine, expire_on_commit=False)
        self.session = self.SessionLocal()

    def close(self):
        self.session.close()
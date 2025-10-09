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

    def __init__(self, base_name: str):
        self.base_name = base_name
        self.db_path = self.BASES_FOLDER / f"{base_name}.db"
        self.BASES_FOLDER.mkdir(exist_ok=True)

        self.engine = create_engine(f"sqlite:///{self.db_path}", connect_args={"check_same_thread": False})
        Base.metadata.create_all(bind=self.engine)

        self.SessionLocal = sessionmaker(bind=self.engine, expire_on_commit=False)
        self.session = self.SessionLocal()

    def commit(self):
        self.session.commit()

    def close(self):
        self.session.close()

    # --- Person ---
    def add_person(self, first_name: str, last_name: str, gender: str = None,
                   birth_date=None, death_date=None, birth_place=None,
                   death_place=None, occupation=None, notes=None):
        person = Person(
            first_name=first_name,
            last_name=last_name,
            gender=gender,
            birth_date=birth_date,
            death_date=death_date,
            birth_place=birth_place,
            death_place=death_place,
            occupation=occupation,
            notes=notes
        )
        self.session.add(person)
        self.commit()
        return person
    
    def get_all_persons(self):
        return self.session.query(Person).all()
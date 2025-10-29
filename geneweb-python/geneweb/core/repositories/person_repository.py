from sqlalchemy.orm import Session
from geneweb.core.models.Person import Person


class PersonRepository:
    def __init__(self, session: Session):
        self.session = session

    def add_person(
        self,
        first_name: str,
        last_name: str,
        gender: str = None,
        birth_date=None,
        death_date=None,
        birth_place=None,
        death_place=None,
        occupation=None,
        notes=None,
    ):
        person = Person(
            first_name=first_name,
            last_name=last_name,
            gender=gender,
            birth_date=birth_date,
            death_date=death_date,
            birth_place=birth_place,
            death_place=death_place,
            occupation=occupation,
            notes=notes,
        )
        self.session.add(person)
        self.session.commit()
        return person

    def get_all_person(self):
        return self.session.query(Person).all()

    def get_a_person_by_id(self, person_id: int):
        return self.session.query(Person).filter(
            Person.id == person_id).first()

    def get_a_person_by_first_name(self, person_first_name: str):
        return (
            self.session.query(Person)
            .filter(Person.first_name == person_first_name)
            .first()
        )

    def update_person(self, person_first_name: str, new_person: Person):
        person = self.get_a_person_by_first_name(person_first_name)
        if not person:
            return None

        for attr, value in vars(new_person).items():
            if attr != "id" and value is not None:
                setattr(person, attr, value)
        self.session.commit()
        return person

    def delete_person_by_first_name(self, first_name: str):
        person = self.get_a_person_by_first_name(first_name)
        if person:
            self.session.delete(person)
            self.session.commit()
            return True
        return False

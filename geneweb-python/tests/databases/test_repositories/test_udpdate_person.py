from conftest import db
from datetime import date
from geneweb.core.repositories.person_repository import PersonRepository
from geneweb.core.models.Person import Person

def test_update_person(db):
    repo = PersonRepository(db.session)

    first_name = "John"
    last_name = "John"
    gender = "M"
    birth_date = date(2000, 7, 14)
    death_date = date(2006, 7, 14)
    birth_place = "Paris"
    death_place = "New York"
    occupation = "Engineer"
    notes = None

    repo.add_person(first_name, last_name, gender, birth_date, death_date, birth_place, death_place, occupation, notes=notes)

    found = repo.get_a_person_by_first_name(first_name)
    assert found is not None

    new_first_name = "Johnny"
    new_last_name = "toto"

    new_person = Person(
        first_name=new_first_name,
        last_name=new_last_name
    )

    upd_person = repo.update_person(first_name, new_person)
    assert upd_person is not None
    assert upd_person.first_name == new_first_name
    assert upd_person.last_name == new_last_name

def test_update_person_not_found(db):
    repo = PersonRepository(db.session)

    first_name = "John"
    new_first_name = "Johnny"
    new_last_name = "toto"

    new_person = Person(
        first_name=new_first_name,
        last_name=new_last_name
    )

    upd_person = repo.update_person(first_name, new_person)
    assert upd_person is None
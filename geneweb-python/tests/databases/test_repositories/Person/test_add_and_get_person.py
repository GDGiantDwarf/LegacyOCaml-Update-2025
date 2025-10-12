import pytest
from conftest import db
from datetime import date
from geneweb.core.repositories.person_repository import PersonRepository

def test_add_and_get_person(db):
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

    repo.add_person(
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

    found = repo.get_a_person_by_first_name(first_name)
    assert found is not None
    assert found.first_name == first_name
    assert found.last_name == last_name
    assert found.gender == gender
    assert found.birth_date == birth_date
    assert found.death_date == death_date
    assert found.birth_place == birth_place
    assert found.death_place == death_place
    assert found.occupation == occupation
    assert found.notes == notes
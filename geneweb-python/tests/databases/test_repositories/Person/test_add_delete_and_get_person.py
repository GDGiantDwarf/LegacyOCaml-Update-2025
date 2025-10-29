import pytest
from conftest import db
from datetime import date
from geneweb.core.repositories.person_repository import PersonRepository


def test_add_delete_and_det_person(db):
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
        notes=notes,
    )

    found = repo.get_a_person_by_first_name(first_name)
    assert found is not None

    repo.delete_person_by_first_name(first_name)

    found = repo.get_a_person_by_first_name(first_name)
    assert found is None


def test_delete_person_not_found(db):
    repo = PersonRepository(db.session)

    first_name = "John"

    result = repo.delete_person_by_first_name(first_name)
    assert result is False

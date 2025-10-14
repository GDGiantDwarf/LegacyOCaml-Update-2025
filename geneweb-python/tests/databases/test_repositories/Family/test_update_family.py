import pytest
from conftest import db
from datetime import date
from geneweb.core.repositories.person_repository import PersonRepository
from geneweb.core.repositories.family_repository import FamilyRepository

def test_add_and_update_a_family(db):
    person_repo = PersonRepository(db.session)
    repo = FamilyRepository(db.session)

    spouse1 = person_repo.add_person(first_name="Alice", last_name="Dupont")
    spouse2 = person_repo.add_person(first_name="Bob", last_name="Martin")
    new_spouse1 = person_repo.add_person(first_name="mickeal", last_name="CA")

    marriage_date = date(2010, 6, 15)
    marriage_place = "Paris"
    divorce_date = None
    notes = "Mariage heureux"

    created = repo.add_family(
        spouse1_id=spouse1.id,
        spouse2_id=spouse2.id,
        marriage_date=marriage_date,
        marriage_place=marriage_place,
        divorce_date=divorce_date,
        notes=notes
    )

    family = repo.get_family_by_id(created.id)
    assert family is not None
    assert family.spouse1_id == spouse1.id
    assert family.spouse2_id == spouse2.id
    assert family.marriage_date == marriage_date
    assert family.marriage_place == marriage_place
    assert family.notes == notes

    updated_family = repo.update_family_by_id(family.id, spouse1_id=new_spouse1)
    assert updated_family is not None

    get_updated_family = repo.get_family_by_id(family.id)
    assert get_updated_family is not None
    assert get_updated_family.spouse1_id == new_spouse1

def test_add_and_update_a_wrong_family(db):
    person_repo = PersonRepository(db.session)
    repo = FamilyRepository(db.session)

    spouse1 = person_repo.add_person(first_name="Alice", last_name="Dupont")
    spouse2 = person_repo.add_person(first_name="Bob", last_name="Martin")
    new_spouse1 = person_repo.add_person(first_name="mickeal", last_name="CA")

    marriage_date = date(2010, 6, 15)
    marriage_place = "Paris"
    divorce_date = None
    notes = "Mariage heureux"

    created = repo.add_family(
        spouse1_id=spouse1.id,
        spouse2_id=spouse2.id,
        marriage_date=marriage_date,
        marriage_place=marriage_place,
        divorce_date=divorce_date,
        notes=notes
    )

    family = repo.get_family_by_id(created.id)
    assert family is not None
    assert family.spouse1_id == spouse1.id
    assert family.spouse2_id == spouse2.id
    assert family.marriage_date == marriage_date
    assert family.marriage_place == marriage_place
    assert family.notes == notes

    with pytest.raises(ValueError) as excinfo:
        repo.update_family_by_id(6, spouse1_id=new_spouse1)

    assert "family_id is invalid" in str(excinfo.value)
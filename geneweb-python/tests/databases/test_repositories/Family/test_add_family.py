from conftest import db
from datetime import date
from geneweb.core.repositories.person_repository import PersonRepository
from geneweb.core.repositories.family_repository import FamilyRepository


def test_add_a_family(db):
    person_repo = PersonRepository(db.session)
    repo = FamilyRepository(db.session)

    spouse1 = person_repo.add_person(first_name="Alice", last_name="Dupont")
    spouse2 = person_repo.add_person(first_name="Bob", last_name="Martin")

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
        notes=notes,
    )

    found = repo.get_family_by_id(created.id)
    assert found is not None
    assert found.spouse1_id == spouse1.id
    assert found.spouse2_id == spouse2.id
    assert found.marriage_date == marriage_date
    assert found.marriage_place == marriage_place
    assert found.notes == notes

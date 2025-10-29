from conftest import db
from datetime import date
from geneweb.core.repositories.person_repository import PersonRepository
from geneweb.core.repositories.family_repository import FamilyRepository


def test_add_one_family_and_delete_it(db):
    person_repo = PersonRepository(db.session)
    repo = FamilyRepository(db.session)

    spouse1 = person_repo.add_person(first_name="Alice", last_name="Dupont")
    spouse2 = person_repo.add_person(first_name="Bob", last_name="Martin")

    created = repo.add_family(spouse1_id=spouse1.id, spouse2_id=spouse2.id)

    found = repo.get_family_by_id(created.id)
    assert found is not None

    result = repo.delete_family(created.id)
    assert result is True

    delete_found = repo.get_family_by_id(created.id)
    assert delete_found is None


def test_add_one_family_and_delete_the_wrong_one(db):
    person_repo = PersonRepository(db.session)
    repo = FamilyRepository(db.session)
    family_id_to_delete = 2

    spouse1 = person_repo.add_person(first_name="Alice", last_name="Dupont")
    spouse2 = person_repo.add_person(first_name="Bob", last_name="Martin")

    created = repo.add_family(spouse1_id=spouse1.id, spouse2_id=spouse2.id)

    found = repo.get_family_by_id(created.id)
    assert found is not None

    result = repo.delete_family(family_id_to_delete)
    assert result is False

    delete_found = repo.get_family_by_id(created.id)
    assert delete_found is not None

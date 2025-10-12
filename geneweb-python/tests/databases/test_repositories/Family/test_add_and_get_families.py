from conftest import db
from geneweb.core.repositories.person_repository import PersonRepository
from geneweb.core.repositories.family_repository import FamilyRepository

def test_add_two_families_and_get_all(db):
    person_repo = PersonRepository(db.session)
    repo = FamilyRepository(db.session)

    spouse1 = person_repo.add_person(first_name="Alice", last_name="Dupont")
    spouse2 = person_repo.add_person(first_name="Bob", last_name="Martin")

    spouse3 = person_repo.add_person(first_name="Lea", last_name="Dupuis")
    spouse4 = person_repo.add_person(first_name="mMrtin", last_name="Bon")

    repo.add_family(spouse1_id=spouse1.id, spouse2_id=spouse2.id)
    repo.add_family(spouse1_id=spouse3.id, spouse2_id=spouse4.id)

    found = repo.get_all_families()
    assert found is not None
    assert len(found) == 2


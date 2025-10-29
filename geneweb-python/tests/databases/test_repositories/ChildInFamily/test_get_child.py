from conftest import db
from geneweb.core.repositories.person_repository import PersonRepository
from geneweb.core.repositories.family_repository import FamilyRepository
from geneweb.core.repositories.child_repository import ChildRepository


def test_add_child_in_a_base(db):
    repo_person = PersonRepository(db.session)
    repo_family = FamilyRepository(db.session)
    repo = ChildRepository(db.session)

    father = repo_person.add_person("tom", "bonjour", "M")
    mother = repo_person.add_person("lily", "truc", "F")
    child = repo_person.add_person("luc", "bonjour", "M")

    family = repo_family.add_family(father.id, mother.id)

    child_family = repo.add_child(child.id, family.id)

    child_family_get = repo.get_child_by_id(child_family.id)
    assert child_family_get is not None
    assert child_family_get.person_id == child_family.person_id
    assert child_family_get.family_id == child_family.family_id

import pytest
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
    assert child_family is not None
    assert child_family.person_id == child.id
    assert child_family.family_id == family.id


def test_add_child_with_none_person_id(db):
    repo_person = PersonRepository(db.session)
    repo_family = FamilyRepository(db.session)
    repo = ChildRepository(db.session)

    father = repo_person.add_person("tom", "bonjour", "M")
    mother = repo_person.add_person("lily", "truc", "F")

    family = repo_family.add_family(father.id, mother.id)

    with pytest.raises(ValueError) as excinfo:
        repo.add_child(person_id=None, family_id=family.id)

    assert "A person_id must be provided" in str(excinfo.value)


def test_add_child_with_none_family_id(db):
    repo_person = PersonRepository(db.session)
    repo = ChildRepository(db.session)

    child = repo_person.add_person("luc", "bonjour", "M")

    with pytest.raises(ValueError) as excinfo:
        repo.add_child(person_id=child.id, family_id=None)

    assert "A family_id must be provided" in str(excinfo.value)

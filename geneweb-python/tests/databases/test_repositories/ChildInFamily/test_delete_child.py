import pytest
from conftest import db
from geneweb.core.repositories.person_repository import PersonRepository
from geneweb.core.repositories.family_repository import FamilyRepository
from geneweb.core.repositories.child_repository import ChildRepository


def test_delete_child_by_id(db):
    repo_person = PersonRepository(db.session)
    repo_family = FamilyRepository(db.session)
    repo = ChildRepository(db.session)

    father = repo_person.add_person("tom", "bonjour", "M")
    mother = repo_person.add_person("lily", "truc", "F")
    child = repo_person.add_person("luc", "bonjour", "M")

    family = repo_family.add_family(father.id, mother.id)

    child_family = repo.add_child(child.id, family.id)

    deleted_child = repo.delete_child_by_id(child_family.id)
    assert deleted_child


def test_delete_child_with_wrong_id(db):
    repo_person = PersonRepository(db.session)
    repo_family = FamilyRepository(db.session)
    repo = ChildRepository(db.session)

    father = repo_person.add_person("tom", "bonjour", "M")
    mother = repo_person.add_person("lily", "truc", "F")
    child = repo_person.add_person("luc", "bonjour", "M")

    family = repo_family.add_family(father.id, mother.id)

    child_family = repo.add_child(child.id, family.id)

    deleted_child = repo.delete_child_by_id(3)
    assert deleted_child is False

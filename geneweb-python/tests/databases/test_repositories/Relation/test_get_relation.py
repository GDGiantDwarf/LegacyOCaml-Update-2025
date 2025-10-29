import pytest
from conftest import db
from geneweb.core.repositories.relation_repository import RelationRepository
from geneweb.core.repositories.person_repository import PersonRepository


def test_get_a_relation(db):
    repo_person = PersonRepository(db.session)
    repo = RelationRepository(db.session)

    person1 = repo_person.add_person("Noe", "gallam")
    person2 = repo_person.add_person("luci", "dubois")

    relation = repo.add_relation(person1.id, person2.id, "amant")
    assert relation is not None
    assert relation.person1_id == person1.id
    assert relation.person2_id == person2.id

    relation_get = repo.get_relation_by_id(relation.id)
    assert relation_get is not None
    assert relation_get.person1_id == relation.person1_id
    assert relation_get.person2_id == relation.person2_id
    assert relation_get.relation_type == relation.relation_type


def test_get_a_wrong_relation(db):
    repo_person = PersonRepository(db.session)
    repo = RelationRepository(db.session)

    person1 = repo_person.add_person("Noe", "gallam")
    person2 = repo_person.add_person("luci", "dubois")

    relation = repo.add_relation(person1.id, person2.id, "amant")
    assert relation is not None
    assert relation.person1_id == person1.id
    assert relation.person2_id == person2.id

    relation_get = repo.get_relation_by_id(4)
    assert relation_get is None

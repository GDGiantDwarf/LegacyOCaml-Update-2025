import pytest
from conftest import db
from geneweb.core.repositories.relation_repository import RelationRepository
from geneweb.core.repositories.person_repository import PersonRepository

def test_add_relation(db):
    repo_person = PersonRepository(db.session)
    repo = RelationRepository(db.session)

    person1 = repo_person.add_person("Noe", "gallam")
    person2 = repo_person.add_person("luci", "dubois")

    relation = repo.add_relation(person1.id, person2.id, "amant")
    assert relation is not None
    assert relation.person1_id == person1.id
    assert relation.person2_id == person2.id

def test_add_relation_person1_none(db):
    repo_person = PersonRepository(db.session)
    repo = RelationRepository(db.session)

    person1 = repo_person.add_person("Noe", "gallam")
    person2 = repo_person.add_person("luci", "dubois")

    with pytest.raises(ValueError) as excinfo:
        repo.add_relation(None, person2.id, "amant")

    assert "person1_id is invalid" in str(excinfo.value)

def test_add_relation_person2_none(db):
    repo_person = PersonRepository(db.session)
    repo = RelationRepository(db.session)

    person1 = repo_person.add_person("Noe", "gallam")
    person2 = repo_person.add_person("luci", "dubois")

    with pytest.raises(ValueError) as excinfo:
        repo.add_relation(person1.id, None, "amant")

    assert "person2_id is invalid" in str(excinfo.value)

def test_add_relation_relation_type_none(db):
    repo_person = PersonRepository(db.session)
    repo = RelationRepository(db.session)

    person1 = repo_person.add_person("Noe", "gallam")
    person2 = repo_person.add_person("luci", "dubois")

    with pytest.raises(ValueError) as excinfo:
        repo.add_relation(person1.id, person2.id, None)

    assert "relation_type is invalid" in str(excinfo.value)

def test_add_relation_relation_type_empty(db):
    repo_person = PersonRepository(db.session)
    repo = RelationRepository(db.session)

    person1 = repo_person.add_person("Noe", "gallam")
    person2 = repo_person.add_person("luci", "dubois")

    with pytest.raises(ValueError) as excinfo:
        repo.add_relation(person1.id, person2.id, "")

    assert "relation_type is invalid" in str(excinfo.value)
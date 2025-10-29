import pytest
from conftest import db
from geneweb.core.repositories.relation_repository import RelationRepository
from geneweb.core.repositories.person_repository import PersonRepository


def test_update_relation(db):
    repo_person = PersonRepository(db.session)
    repo = RelationRepository(db.session)

    person1 = repo_person.add_person("Noe", "gallam")
    person2 = repo_person.add_person("luci", "dubois")

    relation = repo.add_relation(person1.id, person2.id, "amant")
    assert relation is not None
    assert relation.person1_id == person1.id
    assert relation.person2_id == person2.id
    assert relation.relation_type == "amant"

    relation_update = repo.update_relation_by_id(
        relation.id, relation_type="friend")
    assert relation_update is not None
    assert relation_update.person1_id == person1.id
    assert relation_update.person2_id == person2.id
    assert relation_update.relation_type == "friend"


def test_update_relation_with_wrong_relation_id(db):
    repo_person = PersonRepository(db.session)
    repo = RelationRepository(db.session)

    person1 = repo_person.add_person("Noe", "gallam")
    person2 = repo_person.add_person("luci", "dubois")

    relation = repo.add_relation(person1.id, person2.id, "amant")
    assert relation is not None
    assert relation.person1_id == person1.id
    assert relation.person2_id == person2.id
    assert relation.relation_type == "amant"

    with pytest.raises(ValueError) as ecxinfo:
        repo.update_relation_by_id(5, relation_type="friend")

    assert "relation_id Invalid" in str(ecxinfo.value)

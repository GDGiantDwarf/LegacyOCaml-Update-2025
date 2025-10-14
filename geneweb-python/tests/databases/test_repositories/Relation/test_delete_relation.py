import pytest
from conftest import db
from geneweb.core.repositories.relation_repository import RelationRepository
from geneweb.core.repositories.person_repository import PersonRepository

def test_delete_relation(db):
    repo_person = PersonRepository(db.session)
    repo = RelationRepository(db.session)

    person1 = repo_person.add_person("Noe", "gallam")
    person2 = repo_person.add_person("luci", "dubois")

    relation = repo.add_relation(person1.id, person2.id, "amant")
    assert relation is not None
    assert relation.person1_id == person1.id
    assert relation.person2_id == person2.id

    deleted_relation = repo.delete_relation_by_id(relation.id)
    assert deleted_relation == True


def test_delete_relation_with_wrong_id(db):
    repo_person = PersonRepository(db.session)
    repo = RelationRepository(db.session)

    person1 = repo_person.add_person("Noe", "gallam")
    person2 = repo_person.add_person("luci", "dubois")

    relation = repo.add_relation(person1.id, person2.id, "amant")
    assert relation is not None
    assert relation.person1_id == person1.id
    assert relation.person2_id == person2.id

    deleted_relation = repo.delete_relation_by_id(4)
    assert deleted_relation == False
import pytest
from conftest import db
from geneweb.core.repositories.person_repository import PersonRepository
from geneweb.core.repositories.family_repository import FamilyRepository
from geneweb.core.repositories.child_repository import ChildRepository


def test_update_child_with_wrong_child_id(db):
    repo_person = PersonRepository(db.session)
    repo_family = FamilyRepository(db.session)
    repo = ChildRepository(db.session)

    # Creation de deux Personne parents pour creer une famille
    father = repo_person.add_person("tom", "bonjour", "M")
    mother = repo_person.add_person("lily", "truc", "F")

    # Creation de la famille avec les deux parents
    family = repo_family.add_family(father.id, mother.id)

    # Creation d'une Personne enfant
    child = repo_person.add_person("luc", "bonjour", "M")

    # Creation d'une famille avec un enfant de base biologique
    repo.add_child(child.id, family.id, relation_type="Biological")

    # update de la child_family par adopted

    with pytest.raises(ValueError) as excinfo:
        repo.update_child_by_id(4)

    assert "child_family_id Invalid" in str(excinfo.value)


def test_update_relation_type_in_child_family(db):
    repo_person = PersonRepository(db.session)
    repo_family = FamilyRepository(db.session)
    repo = ChildRepository(db.session)

    # Creation de deux Personne parents pour creer une famille
    father = repo_person.add_person("tom", "bonjour", "M")
    mother = repo_person.add_person("lily", "truc", "F")

    # Creation de la famille avec les deux parents
    family = repo_family.add_family(father.id, mother.id)

    # Creation d'une Personne enfant
    child = repo_person.add_person("luc", "bonjour", "M")

    # Creation d'une famille avec un enfant de base biologique
    child_family = repo.add_child(
        child.id, family.id, relation_type="Biological")

    # update de la child_family par adopted
    updated_child_family = repo.update_child_by_id(
        child_family.id, relation_type="adopted"
    )

    assert updated_child_family is not None
    assert updated_child_family.person_id == child_family.person_id
    assert updated_child_family.family_id == child_family.family_id
    assert updated_child_family.relation_type == "adopted"


def test_update_family_id_in_child_family(db):
    repo_person = PersonRepository(db.session)
    repo_family = FamilyRepository(db.session)
    repo = ChildRepository(db.session)

    # Creation de deux Personne parents pour creer une famille
    father = repo_person.add_person("tom", "bonjour", "M")
    mother = repo_person.add_person("lily", "truc", "F")

    # Creation de la famille avec les deux parents
    family = repo_family.add_family(father.id, mother.id)

    # Creation d'une Personne enfant
    child = repo_person.add_person("luc", "bonjour", "M")

    # Creation d'une famille avec un enfant de base biologique
    child_family = repo.add_child(
        child.id, family.id, relation_type="Biological")

    # Creation d'une deuxieme famille
    # Creation de deux Personne parents pour creer une famille
    new_father = repo_person.add_person("Martin", "bonjour", "M")
    new_mother = repo_person.add_person("Lilian", "truc", "F")

    # Creation de la famille avec les deux parents
    new_family = repo_family.add_family(new_father.id, new_mother.id)

    # update de la child_family par adopted
    updated_child_family = repo.update_child_by_id(
        child_family.id, family_id=new_family.id
    )

    assert updated_child_family is not None
    assert updated_child_family.person_id == child.id
    assert updated_child_family.family_id == new_family.id
    assert updated_child_family.relation_type == "Biological"


def test_update_child_id_in_child_family(db):
    repo_person = PersonRepository(db.session)
    repo_family = FamilyRepository(db.session)
    repo = ChildRepository(db.session)

    # Creation de deux Personne parents pour creer une famille
    father = repo_person.add_person("tom", "bonjour", "M")
    mother = repo_person.add_person("lily", "truc", "F")

    # Creation de la famille avec les deux parents
    family = repo_family.add_family(father.id, mother.id)

    # Creation d'une Personne enfant
    child = repo_person.add_person("luc", "bonjour", "M")

    # Creation d'une famille avec un enfant de base biologique
    child_family = repo.add_child(
        child.id, family.id, relation_type="Biological")

    # Creation d'une nouvelle Personne enfant pour remplacer l'ancien
    new_child = repo_person.add_person("luc", "bonjour", "M")

    # update de la child_family par adopted
    updated_child_family = repo.update_child_by_id(
        child_family.id, person_id=new_child.id
    )

    assert updated_child_family is not None
    assert updated_child_family.person_id == new_child.id
    assert updated_child_family.family_id == family.id
    assert updated_child_family.relation_type == "Biological"

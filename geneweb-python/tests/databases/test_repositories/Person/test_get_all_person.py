from conftest import db
from geneweb.core.repositories.person_repository import PersonRepository

def test_get_all_person_in_a_empyt_base(db):
    repo = PersonRepository(db.session)

    list = repo.get_all_person()
    print(list)

    assert list == []

def test_get_all_person_in_a_base_with_one_person(db):
    repo = PersonRepository(db.session)

    first_name = "Johnny"
    last_name = "toto"

    repo.add_person(first_name, last_name)

    persons = repo.get_all_person()

    assert len(persons) == 1

def test_get_all_person_in_a_base_with_four_person(db):
    repo = PersonRepository(db.session)
    nb_person = 4

    first_name = "Johnny"
    last_name = "toto"

    for j in range(nb_person):
        repo.add_person(first_name, last_name)

    persons = repo.get_all_person()

    assert len(persons) == nb_person




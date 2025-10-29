from conftest import db
from geneweb.core.repositories.person_repository import PersonRepository


def test_get_a_person_by_id(db):
    repo = PersonRepository(db.session)

    first_name = "Johnny"
    last_name = "toto"

    person = repo.add_person(first_name, last_name)
    assert person is not None

    found = repo.get_a_person_by_id(person.id)
    assert found.first_name == first_name
    assert found.last_name == last_name

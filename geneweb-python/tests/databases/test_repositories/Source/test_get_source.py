from conftest import db
from datetime import date
from geneweb.core.repositories.source_repository import SourceRepository

def test_add_one_source_and_get_it(db):
    repo = SourceRepository(db.session)

    title = "title"
    reference = "reference"
    type = "mp4"

    source = repo.add_source(title, reference, type)
    assert source is not None

    sources = repo.get_source_by_id(source.id)
    assert sources is not None
    assert sources.title == title
    assert sources.reference == reference
    assert sources.type == type


def test_add_one_source_and_get_a_wrong_one(db):
    repo = SourceRepository(db.session)

    title = "title"
    reference = "reference"
    type = "mp4"

    source = repo.add_source(title, reference, type)
    assert source is not None

    sources = repo.get_source_by_id(5)
    assert sources is None
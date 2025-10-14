from conftest import db
from datetime import date
from geneweb.core.repositories.source_repository import SourceRepository

def test_add_and_delete_an_event(db):
    repo = SourceRepository(db.session)

    title = "title"
    reference = "reference"
    type = "mp4"

    source = repo.add_source(title, reference, type)
    assert source is not None

    event_deleted = repo.delete_source_by_id(source.id)
    assert event_deleted == True

def test_add_and_delete_a_wrong_event(db):
    repo = SourceRepository(db.session)

    title = "title"
    reference = "reference"
    type = "mp4"

    source = repo.add_source(title, reference, type)
    assert source is not None

    event_deleted = repo.delete_source_by_id(5)
    assert event_deleted == False
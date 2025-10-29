import pytest
from conftest import db
from geneweb.core.repositories.source_repository import SourceRepository


def test_update_source(db):
    repo = SourceRepository(db.session)

    title = "title"
    reference = "reference"
    type = "mp4"
    type_update = "mp3"

    source = repo.add_source(title, reference, type)
    assert source is not None

    source_upd = repo.update_source_by_id(source.id, type=type_update)
    assert source_upd is not None
    assert source_upd.type == type_update


def test_update_event_with_wrong_source_id(db):
    repo = SourceRepository(db.session)

    title = "title"
    reference = "reference"
    type = "mp4"
    type_update = "mp3"

    source = repo.add_source(title, reference, type)
    assert source is not None

    with pytest.raises(ValueError) as ecxconfig:
        repo.update_source_by_id(5, type=type_update)

    assert "source_id is invalid" in str(ecxconfig.value)

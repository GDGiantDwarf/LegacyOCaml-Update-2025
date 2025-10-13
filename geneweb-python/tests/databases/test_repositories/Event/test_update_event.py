import pytest
from conftest import db
from datetime import date
from geneweb.core.repositories.event_repository import EventRepository

def test_update_event(db):
    repo = EventRepository(db.session)
    event_type = "marriage"
    event_type_update = "Divorced"

    event = repo.add_event(event_type=event_type)
    assert event is not None
    assert event.event_type == event_type
    assert event.event_type == event_type

    event_upd = repo.update_event_by_id(event.id, event_type=event_type_update)
    assert event_upd is not None
    assert event_upd.event_type == event_type_update

def test_update_event_with_wrong_event_id(db):
    repo = EventRepository(db.session)
    event_type = "marriage"
    event_type_update = "Divorced"

    event = repo.add_event(event_type=event_type)
    assert event is not None
    assert event.event_type == event_type
    assert event.event_type == event_type

    with pytest.raises(ValueError) as ecxconfig:
        repo.update_event_by_id(5, event_type=event_type_update)

    assert "event_id is invalid" in str(ecxconfig.value)
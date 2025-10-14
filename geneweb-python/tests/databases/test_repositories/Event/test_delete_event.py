import pytest
from conftest import db
from datetime import date
from geneweb.core.repositories.event_repository import EventRepository

def test_add_and_delete_an_event(db):
    repo = EventRepository(db.session)
    event_type = "marriage"

    event = repo.add_event(event_type=event_type)
    assert event is not None
    assert event.event_type == event_type
    assert event.event_type == event_type

    event_deleted = repo.delete_event_by_id(event.id)
    assert event_deleted == True

def test_add_and_delete_a_wrong_event(db):
    repo = EventRepository(db.session)
    event_type = "marriage"

    event = repo.add_event(event_type=event_type)
    assert event is not None
    assert event.event_type == event_type
    assert event.event_type == event_type

    event_deleted = repo.delete_event_by_id(5)
    assert event_deleted == False

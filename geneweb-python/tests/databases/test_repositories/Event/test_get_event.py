from conftest import db
from datetime import date
from geneweb.core.repositories.event_repository import EventRepository


def test_add_one_event_and_get_it(db):
    repo = EventRepository(db.session)
    event_type = "marriage"

    event = repo.add_event(event_type=event_type)
    assert event is not None

    events = repo.get_event_by_id(event.id)
    assert events is not None
    assert events.event_type == event_type


def test_add_one_event_and_get_a_wrong_one(db):
    repo = EventRepository(db.session)
    event_type = "marriage"

    event = repo.add_event(event_type=event_type)
    assert event is not None

    events = repo.get_event_by_id(5)
    print(events)
    assert events is None

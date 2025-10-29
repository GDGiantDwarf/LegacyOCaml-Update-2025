from conftest import db
from datetime import date
from geneweb.core.repositories.event_repository import EventRepository


def test_add_one_event(db):
    repo = EventRepository(db.session)

    event = repo.add_event(event_type="marriage")
    assert event is not None

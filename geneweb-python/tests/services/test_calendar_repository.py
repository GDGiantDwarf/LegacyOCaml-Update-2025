from geneweb.core.database import Database
from geneweb.core.repositories.calendar_repository import (
    CalendarRepository,
)


def _make_repo():
    """Create a CalendarRepository with in-memory DB."""
    db = Database(in_memory=True)
    repo = CalendarRepository(db.session)
    return db, repo


def test_add_calendar_date():
    db, repo = _make_repo()
    cd = repo.add_calendar_date(
        person_id=None,
        event_type="birth",
        gregorian_year=2000,
        gregorian_month=6,
        gregorian_day=15,
    )
    assert cd.id is not None
    assert cd.event_type == "birth"
    assert cd.gregorian_year == 2000
    assert cd.gregorian_month == 6
    assert cd.gregorian_day == 15
    assert cd.julian_year is not None
    assert cd.hebrew_year is not None
    db.close()


def test_get_by_person():
    db, repo = _make_repo()
    repo.add_calendar_date(
        person_id=42,
        event_type="birth",
        gregorian_year=1990,
        gregorian_month=1,
        gregorian_day=1,
    )
    repo.add_calendar_date(
        person_id=42,
        event_type="death",
        gregorian_year=2050,
        gregorian_month=12,
        gregorian_day=31,
    )
    results = repo.get_calendar_dates_by_person(42)
    assert len(results) == 2
    types = {r.event_type for r in results}
    assert types == {"birth", "death"}
    db.close()


def test_get_by_id():
    db, repo = _make_repo()
    cd = repo.add_calendar_date(
        person_id=None,
        event_type="marriage",
        gregorian_year=2010,
        gregorian_month=7,
        gregorian_day=4,
    )
    fetched = repo.get_calendar_date_by_id(cd.id)
    assert fetched is not None
    assert fetched.event_type == "marriage"
    assert fetched.gregorian_year == 2010
    db.close()


def test_delete():
    db, repo = _make_repo()
    cd = repo.add_calendar_date(
        person_id=None,
        event_type="baptism",
        gregorian_year=1800,
        gregorian_month=3,
        gregorian_day=25,
    )
    date_id = cd.id
    deleted = repo.delete_calendar_date(date_id)
    assert deleted is True
    gone = repo.get_calendar_date_by_id(date_id)
    assert gone is None
    db.close()

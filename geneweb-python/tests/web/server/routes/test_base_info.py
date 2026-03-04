"""Tests for the public server base_info routes."""

import sqlite3

import pytest
from fastapi.testclient import TestClient

from geneweb.web.server.server import create_app


def _create_test_db(db_dir, name="testbase"):
    """Create a populated SQLite test database."""
    from datetime import date as dt_date
    today = dt_date.today()
    mm = f"{today.month:02d}"
    dd = f"{today.day:02d}"
    today_str = f"1990-{mm}-{dd}"
    month_str = f"1985-{mm}-15"

    db_path = db_dir / f"{name}.db"
    con = sqlite3.connect(str(db_path))
    con.execute(
        "CREATE TABLE persons ("
        "id INTEGER PRIMARY KEY,"
        "first_name TEXT, last_name TEXT,"
        "gender TEXT, birth_date TEXT,"
        "death_date TEXT, birth_place TEXT,"
        "death_place TEXT, occupation TEXT,"
        "notes TEXT)"
    )
    con.execute(
        "CREATE TABLE families ("
        "id INTEGER PRIMARY KEY,"
        "spouse1_id INTEGER,"
        "spouse2_id INTEGER,"
        "marriage_date TEXT,"
        "marriage_place TEXT,"
        "divorce_date TEXT, notes TEXT)"
    )
    con.execute(
        "CREATE TABLE children_in_family ("
        "id INTEGER PRIMARY KEY,"
        "person_id INTEGER,"
        "family_id INTEGER,"
        "relation_type TEXT)"
    )
    con.execute(
        "CREATE TABLE events ("
        "id INTEGER PRIMARY KEY,"
        "event_type TEXT, date TEXT,"
        "place TEXT, description TEXT,"
        "person_id INTEGER,"
        "family_id INTEGER,"
        "source_id INTEGER)"
    )
    con.execute(
        "CREATE TABLE notes ("
        "id INTEGER PRIMARY KEY,"
        "content TEXT, person_id INTEGER,"
        "event_id INTEGER)"
    )
    con.execute(
        "CREATE TABLE sources ("
        "id INTEGER PRIMARY KEY,"
        "title TEXT, reference TEXT,"
        "type TEXT, repository TEXT,"
        "notes TEXT)"
    )
    con.execute(
        "CREATE TABLE media ("
        "id INTEGER PRIMARY KEY,"
        "file_path TEXT, description TEXT,"
        "linked_person_id INTEGER,"
        "linked_event_id INTEGER)"
    )
    # Person born today (for anniversary tests)
    con.execute(
        "INSERT INTO persons VALUES "
        f"(1,'John','Smith','M','{today_str}',"
        "NULL,'Paris',NULL,'Engineer',NULL)"
    )
    # Person with death this month
    con.execute(
        "INSERT INTO persons VALUES "
        "(2,'Jane','Smith','F','1992-03-20',"
        f"'{month_str}','Lyon',NULL,NULL,NULL)"
    )
    # Person with birth and death
    con.execute(
        "INSERT INTO persons VALUES "
        "(3,'Bob','Doe','M','1985-06-10',"
        "'2070-01-01','Marseille','Nice',"
        "'Doctor',NULL)"
    )
    # Unknown gender person
    con.execute(
        "INSERT INTO persons VALUES "
        "(4,'Pat','Unk','X','2000-01-01',"
        "NULL,NULL,NULL,NULL,NULL)"
    )
    # Marriage today
    con.execute(
        "INSERT INTO families VALUES "
        f"(1,1,2,'{today_str}','Paris',NULL,NULL)"
    )
    con.execute(
        "INSERT INTO children_in_family VALUES "
        "(1,3,1,'biological')"
    )
    # Events: baptism and burial
    con.execute(
        "INSERT INTO events VALUES "
        "(1,'birth','1990-01-15','Paris',"
        "'Born',1,NULL,NULL)"
    )
    con.execute(
        "INSERT INTO events VALUES "
        "(2,'baptism','1990-02-01','Chartres',"
        "'Baptized',1,NULL,NULL)"
    )
    con.execute(
        "INSERT INTO events VALUES "
        "(3,'burial','2070-01-05','Nice',"
        "'Buried',3,NULL,NULL)"
    )
    con.commit()
    con.close()
    return db_path


@pytest.fixture()
def populated_db(tmp_path, monkeypatch):
    """Set up a temp dir with a populated SQLite DB."""
    _create_test_db(tmp_path)
    monkeypatch.setattr(
        "geneweb.core.database.BaseManager.bases_dir",
        staticmethod(
            lambda base_dir=None: tmp_path
        ),
    )
    return tmp_path


@pytest.fixture()
def client():
    """Create a fresh TestClient."""
    app = create_app()
    return TestClient(app)


# ---------------------------------------------------------
# Statistics
# ---------------------------------------------------------

def test_stats_page(client, populated_db):
    """GET /base/testbase/stats returns 200 HTML."""
    response = client.get("/base/testbase/stats")
    assert response.status_code == 200
    content_type = response.headers["content-type"]
    assert "text/html" in content_type


# ---------------------------------------------------------
# Anniversaries
# ---------------------------------------------------------

def test_anniversaries(client, populated_db):
    """GET /base/testbase/anniversaries returns 200."""
    response = client.get(
        "/base/testbase/anniversaries"
    )
    assert response.status_code == 200
    content_type = response.headers["content-type"]
    assert "text/html" in content_type


# ---------------------------------------------------------
# Places
# ---------------------------------------------------------

def test_places(client, populated_db):
    """GET /base/testbase/places returns 200 HTML."""
    response = client.get("/base/testbase/places")
    assert response.status_code == 200
    content_type = response.headers["content-type"]
    assert "text/html" in content_type


# ---------------------------------------------------------
# Config
# ---------------------------------------------------------

def test_config(client, populated_db):
    """GET /base/testbase/config returns 200 HTML."""
    response = client.get("/base/testbase/config")
    assert response.status_code == 200
    content_type = response.headers["content-type"]
    assert "text/html" in content_type


def test_config_post(client, populated_db):
    """POST /base/testbase/config returns 200."""
    r = client.post("/base/testbase/config")
    assert r.status_code == 200


def test_config_nonexistent(client, populated_db):
    """GET config for missing base returns 200."""
    r = client.get("/base/nosuchbase/config")
    assert r.status_code == 200


# ---------------------------------------------------------
# Stats on nonexistent base
# ---------------------------------------------------------

def test_stats_nonexistent(client, populated_db):
    """GET stats on missing base returns 200."""
    r = client.get("/base/nosuchbase/stats")
    assert r.status_code == 200


# ---------------------------------------------------------
# Anniversaries on nonexistent base
# ---------------------------------------------------------

def test_anniversaries_nonexistent(
    client, populated_db
):
    """GET anniv on missing base returns 200."""
    r = client.get(
        "/base/nosuchbase/anniversaries"
    )
    assert r.status_code == 200


# ---------------------------------------------------------
# Places with filters
# ---------------------------------------------------------

def test_places_filter_birth_only(
    client, populated_db
):
    """GET places with only birth filter."""
    r = client.get(
        "/base/testbase/places"
        "?bi=on&ba=off&ma=off&de=off&bu=off"
    )
    assert r.status_code == 200


def test_places_filter_death_only(
    client, populated_db
):
    """GET places with only death filter."""
    r = client.get(
        "/base/testbase/places"
        "?bi=off&ba=off&ma=off&de=on&bu=off"
    )
    assert r.status_code == 200


def test_places_filter_marriage(
    client, populated_db
):
    """GET places with marriage filter."""
    r = client.get(
        "/base/testbase/places"
        "?bi=off&ba=off&ma=on&de=off&bu=off"
    )
    assert r.status_code == 200


def test_places_nonexistent(
    client, populated_db
):
    """GET places on missing base returns 200."""
    r = client.get("/base/nosuchbase/places")
    assert r.status_code == 200

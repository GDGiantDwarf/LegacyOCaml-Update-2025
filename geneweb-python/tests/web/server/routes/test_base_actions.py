"""Tests for the public server base_actions routes."""

import sqlite3

import pytest
from fastapi.testclient import TestClient

from geneweb.web.server.server import create_app


def _create_test_db(db_dir, name="testbase"):
    """Create a populated SQLite test database."""
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
    # Sample persons
    con.execute(
        "INSERT INTO persons VALUES "
        "(1,'John','Smith','M','1990-01-15',"
        "NULL,'Paris',NULL,'Engineer',NULL)"
    )
    con.execute(
        "INSERT INTO persons VALUES "
        "(2,'Jane','Smith','F','1992-03-20',"
        "NULL,'Lyon',NULL,NULL,NULL)"
    )
    con.execute(
        "INSERT INTO persons VALUES "
        "(3,'Bob','Doe','M','1985-06-10',"
        "'2070-01-01','Marseille','Nice',"
        "'Doctor',NULL)"
    )
    # Sample family
    con.execute(
        "INSERT INTO families VALUES "
        "(1,1,2,'2015-06-20','Paris',NULL,NULL)"
    )
    # Sample child link
    con.execute(
        "INSERT INTO children_in_family VALUES "
        "(1,3,1,'biological')"
    )
    # Sample event
    con.execute(
        "INSERT INTO events VALUES "
        "(1,'birth','1990-01-15','Paris',"
        "'Born',1,NULL,NULL)"
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
# Base details
# ---------------------------------------------------------

def test_base_details_200(client, populated_db):
    """GET /base/testbase returns 200 HTML."""
    response = client.get("/base/testbase")
    assert response.status_code == 200
    content_type = response.headers["content-type"]
    assert "text/html" in content_type


def test_base_details_nonexistent(client, populated_db):
    """GET /base/nosuchbase returns 200 with 0 persons."""
    response = client.get("/base/nosuchbase")
    assert response.status_code == 200
    content_type = response.headers["content-type"]
    assert "text/html" in content_type


# ---------------------------------------------------------
# Search (?m=S)
# ---------------------------------------------------------

def test_search(client, populated_db):
    """GET /base/testbase?m=S&n=Smith returns results."""
    response = client.get(
        "/base/testbase?m=S&n=Smith"
    )
    assert response.status_code == 200
    content_type = response.headers["content-type"]
    assert "text/html" in content_type


# ---------------------------------------------------------
# Surname list (?m=N)
# ---------------------------------------------------------

def test_surname_list_alpha(client, populated_db):
    """GET /base/testbase?m=N&tri=A returns 200."""
    response = client.get(
        "/base/testbase?m=N&tri=A"
    )
    assert response.status_code == 200
    content_type = response.headers["content-type"]
    assert "text/html" in content_type


def test_surname_list_freq(client, populated_db):
    """GET /base/testbase?m=N&tri=F returns 200."""
    response = client.get(
        "/base/testbase?m=N&tri=F"
    )
    assert response.status_code == 200
    content_type = response.headers["content-type"]
    assert "text/html" in content_type


# ---------------------------------------------------------
# First-name list (?m=P)
# ---------------------------------------------------------

def test_firstname_list(client, populated_db):
    """GET /base/testbase?m=P&tri=A returns 200."""
    response = client.get(
        "/base/testbase?m=P&tri=A"
    )
    assert response.status_code == 200
    content_type = response.headers["content-type"]
    assert "text/html" in content_type


# ---------------------------------------------------------
# Titles list (?m=TT)
# ---------------------------------------------------------

def test_titles_list(client, populated_db):
    """GET /base/testbase?m=TT returns 200."""
    response = client.get("/base/testbase?m=TT")
    assert response.status_code == 200
    content_type = response.headers["content-type"]
    assert "text/html" in content_type


# ---------------------------------------------------------
# Advanced search (?m=AS)
# ---------------------------------------------------------

def test_advanced_search(client, populated_db):
    """GET /base/testbase?m=AS returns 200."""
    response = client.get("/base/testbase?m=AS")
    assert response.status_code == 200
    content_type = response.headers["content-type"]
    assert "text/html" in content_type


# ---------------------------------------------------------
# Individual detail (?i=)
# ---------------------------------------------------------

def test_individual_detail(client, populated_db):
    """GET /base/testbase?i=1 returns 200."""
    response = client.get("/base/testbase?i=1")
    assert response.status_code == 200
    content_type = response.headers["content-type"]
    assert "text/html" in content_type


def test_individual_random(client, populated_db):
    """GET /base/testbase?i=random returns 200."""
    response = client.get("/base/testbase?i=random")
    assert response.status_code == 200
    content_type = response.headers["content-type"]
    assert "text/html" in content_type


# ---------------------------------------------------------
# Unknown mode
# ---------------------------------------------------------

def test_unknown_mode(client, populated_db):
    """GET /base/testbase?m=UNKNOWN falls back to details."""
    response = client.get(
        "/base/testbase?m=UNKNOWN"
    )
    assert response.status_code == 200
    content_type = response.headers["content-type"]
    assert "text/html" in content_type


# ---------------------------------------------------------
# Extended search params
# ---------------------------------------------------------

def test_search_firstname(client, populated_db):
    """Search by firstname."""
    r = client.get(
        "/base/testbase?m=S&p=John"
    )
    assert r.status_code == 200


def test_search_birth_place(client, populated_db):
    """Search by birth place."""
    r = client.get(
        "/base/testbase"
        "?m=S&birth_place=Paris"
    )
    assert r.status_code == 200


def test_search_death_place(client, populated_db):
    """Search by death place."""
    r = client.get(
        "/base/testbase"
        "?m=S&death_place=Nice"
    )
    assert r.status_code == 200


def test_search_occupation(client, populated_db):
    """Search by occupation."""
    r = client.get(
        "/base/testbase?m=S&occu=Engineer"
    )
    assert r.status_code == 200


def test_search_birth_year_range(
    client, populated_db
):
    """Search by birth year range."""
    r = client.get(
        "/base/testbase"
        "?m=S&birth_y1=1980&birth_y2=2000"
    )
    assert r.status_code == 200


def test_search_nonexistent_base(
    client, populated_db
):
    """Search on nonexistent base returns 200."""
    r = client.get(
        "/base/nosuchbase?m=S&n=Smith"
    )
    assert r.status_code == 200


def test_titles_detail_mode(client, populated_db):
    """Titles with a specific title filter."""
    r = client.get(
        "/base/testbase?m=TT&t=Engineer"
    )
    assert r.status_code == 200


def test_titles_with_fief(client, populated_db):
    """Titles with fief filter."""
    r = client.get(
        "/base/testbase?m=TT&t=Doctor&v=Nice"
    )
    assert r.status_code == 200


def test_firstname_list_freq(client, populated_db):
    """First-name list by frequency."""
    r = client.get(
        "/base/testbase?m=P&tri=F"
    )
    assert r.status_code == 200


def test_individual_nonexistent(
    client, populated_db
):
    """Individual with bad id returns 200."""
    r = client.get("/base/testbase?i=9999")
    assert r.status_code == 200


def test_individual_random_empty_base(
    client, populated_db
):
    """Random on base with no persons."""
    r = client.get("/base/nosuchbase?i=random")
    assert r.status_code == 200

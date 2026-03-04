"""Tests for the public server base_data routes."""

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
    con.execute(
        "INSERT INTO families VALUES "
        "(1,1,2,'2015-06-20','Paris',NULL,NULL)"
    )
    con.execute(
        "INSERT INTO children_in_family VALUES "
        "(1,3,1,'biological')"
    )
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
# Add Family
# ---------------------------------------------------------

def test_add_family_form(client, populated_db):
    """GET /base/testbase/add-family returns 200."""
    response = client.get(
        "/base/testbase/add-family"
    )
    assert response.status_code == 200
    content_type = response.headers["content-type"]
    assert "text/html" in content_type


def test_add_family_submit(client, populated_db):
    """POST /base/testbase/add-family redirects 303."""
    form_data = {
        "sp1_first_name": "Alice",
        "sp1_last_name": "Martin",
        "sp1_gender": "F",
        "sp2_first_name": "Pierre",
        "sp2_last_name": "Martin",
        "sp2_gender": "M",
        "marriage_date": "2020-05-10",
        "marriage_place": "Bordeaux",
    }
    response = client.post(
        "/base/testbase/add-family",
        data=form_data,
        follow_redirects=False,
    )
    assert response.status_code == 303


def test_add_family_nonexistent_base(
    client, populated_db
):
    """GET /base/nosuchbase/add-family returns 404."""
    response = client.get(
        "/base/nosuchbase/add-family"
    )
    assert response.status_code == 404


# ---------------------------------------------------------
# Notes
# ---------------------------------------------------------

def test_notes_list(client, populated_db):
    """GET /base/testbase/notes returns 200 HTML."""
    response = client.get("/base/testbase/notes")
    assert response.status_code == 200
    content_type = response.headers["content-type"]
    assert "text/html" in content_type


def test_notes_submit(client, populated_db):
    """POST /base/testbase/notes redirects on success."""
    form_data = {"content": "A test note"}
    response = client.post(
        "/base/testbase/notes",
        data=form_data,
        follow_redirects=False,
    )
    assert response.status_code == 303


def test_notes_nonexistent_base(
    client, populated_db
):
    """GET /base/nosuchbase/notes returns 404."""
    response = client.get("/base/nosuchbase/notes")
    assert response.status_code == 404


# ---------------------------------------------------------
# Books
# ---------------------------------------------------------

def test_book_list_fn(client, populated_db):
    """GET /base/testbase/book/fn returns 200."""
    response = client.get("/base/testbase/book/fn")
    assert response.status_code == 200
    content_type = response.headers["content-type"]
    assert "text/html" in content_type


def test_book_list_sn(client, populated_db):
    """GET /base/testbase/book/sn returns 200."""
    response = client.get("/base/testbase/book/sn")
    assert response.status_code == 200
    content_type = response.headers["content-type"]
    assert "text/html" in content_type


def test_book_invalid(client, populated_db):
    """GET /base/testbase/book/invalid returns 400."""
    response = client.get(
        "/base/testbase/book/invalid"
    )
    assert response.status_code == 400


# ---------------------------------------------------------
# More books
# ---------------------------------------------------------

def test_book_place(client, populated_db):
    """GET /base/testbase/book/place returns 200."""
    r = client.get("/base/testbase/book/place")
    assert r.status_code == 200


def test_book_occu(client, populated_db):
    """GET /base/testbase/book/occu returns 200."""
    r = client.get("/base/testbase/book/occu")
    assert r.status_code == 200


def test_book_src(client, populated_db):
    """GET /base/testbase/book/src returns 200."""
    r = client.get("/base/testbase/book/src")
    assert r.status_code == 200


def test_book_nonexistent_base(
    client, populated_db
):
    """GET /base/nosuchbase/book/fn returns 404."""
    r = client.get("/base/nosuchbase/book/fn")
    assert r.status_code == 404


# ---------------------------------------------------------
# POST books
# ---------------------------------------------------------

def test_book_submit_fn(client, populated_db):
    """POST book rename a firstname."""
    r = client.post(
        "/base/testbase/book/fn",
        data={
            "old_value": "John",
            "new_value": "Jonathan",
        },
        follow_redirects=False,
    )
    assert r.status_code == 303


def test_book_submit_sn(client, populated_db):
    """POST book rename a surname."""
    r = client.post(
        "/base/testbase/book/sn",
        data={
            "old_value": "Smith",
            "new_value": "Smithson",
        },
        follow_redirects=False,
    )
    assert r.status_code == 303


def test_book_submit_place(client, populated_db):
    """POST book rename a place."""
    r = client.post(
        "/base/testbase/book/place",
        data={
            "old_value": "Paris",
            "new_value": "Paris, France",
        },
        follow_redirects=False,
    )
    assert r.status_code == 303


def test_book_submit_occu(client, populated_db):
    """POST book rename an occupation."""
    r = client.post(
        "/base/testbase/book/occu",
        data={
            "old_value": "Engineer",
            "new_value": "Software Engineer",
        },
        follow_redirects=False,
    )
    assert r.status_code == 303


def test_book_submit_src(client, populated_db):
    """POST add a source."""
    r = client.post(
        "/base/testbase/book/src",
        data={
            "title": "Archives",
            "reference": "REF001",
            "type": "document",
        },
        follow_redirects=False,
    )
    assert r.status_code == 303


def test_book_submit_src_empty_fields(
    client, populated_db
):
    """POST source with missing fields redirects."""
    r = client.post(
        "/base/testbase/book/src",
        data={
            "title": "",
            "reference": "",
            "type": "",
        },
        follow_redirects=False,
    )
    assert r.status_code == 303


def test_book_submit_empty_value(
    client, populated_db
):
    """POST book with empty new_value redirects."""
    r = client.post(
        "/base/testbase/book/fn",
        data={
            "old_value": "John",
            "new_value": "",
        },
        follow_redirects=False,
    )
    assert r.status_code == 303


def test_book_submit_invalid_type(
    client, populated_db
):
    """POST book with invalid type returns 400."""
    r = client.post(
        "/base/testbase/book/invalid",
        data={
            "old_value": "x",
            "new_value": "y",
        },
    )
    assert r.status_code == 400


def test_book_submit_nonexistent_base(
    client, populated_db
):
    """POST book on nonexistent base returns 404."""
    r = client.post(
        "/base/nosuchbase/book/fn",
        data={
            "old_value": "x",
            "new_value": "y",
        },
    )
    assert r.status_code == 404


# ---------------------------------------------------------
# Notes with person_id
# ---------------------------------------------------------

def test_notes_submit_with_person(
    client, populated_db
):
    """POST note with person_id."""
    r = client.post(
        "/base/testbase/notes",
        data={
            "content": "A note for person",
            "person_id": "1",
        },
        follow_redirects=False,
    )
    assert r.status_code == 303


def test_notes_submit_empty_content(
    client, populated_db
):
    """POST note with empty content redirects."""
    r = client.post(
        "/base/testbase/notes",
        data={"content": ""},
        follow_redirects=False,
    )
    assert r.status_code == 303


def test_notes_submit_update(client, populated_db):
    """POST update an existing note."""
    # First insert a note
    con = sqlite3.connect(
        str(populated_db / "testbase.db")
    )
    con.execute(
        "INSERT INTO notes (id, content) "
        "VALUES (1, 'Original')"
    )
    con.commit()
    con.close()

    r = client.post(
        "/base/testbase/notes",
        data={
            "content": "Updated note",
            "note_id": "1",
        },
        follow_redirects=False,
    )
    assert r.status_code == 303


def test_notes_post_nonexistent_base(
    client, populated_db
):
    """POST notes on nonexistent base returns 404."""
    r = client.post(
        "/base/nosuchbase/notes",
        data={"content": "test"},
    )
    assert r.status_code == 404


# ---------------------------------------------------------
# Add family with children
# ---------------------------------------------------------

def test_add_family_with_children(
    client, populated_db
):
    """POST add-family with child data."""
    form = {
        "sp1_first_name": "Marc",
        "sp1_last_name": "Dupont",
        "sp1_gender": "M",
        "sp2_first_name": "Marie",
        "sp2_last_name": "Dupont",
        "sp2_gender": "F",
        "child_0_first_name": "Luc",
        "child_0_last_name": "Dupont",
        "child_0_gender": "M",
    }
    r = client.post(
        "/base/testbase/add-family",
        data=form,
        follow_redirects=False,
    )
    assert r.status_code == 303


def test_add_family_post_nonexistent(
    client, populated_db
):
    """POST add-family on missing base -> 404."""
    r = client.post(
        "/base/nosuchbase/add-family",
        data={
            "sp1_first_name": "X",
            "sp1_last_name": "Y",
            "sp2_first_name": "A",
            "sp2_last_name": "B",
        },
    )
    assert r.status_code == 404

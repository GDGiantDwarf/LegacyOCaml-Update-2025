import sqlite3
import os
import io
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
import pytest
from fastapi.testclient import TestClient
from geneweb.web.admin.server import create_app
from geneweb.core.database import BaseManager
# Ensure all ORM models are registered so
# SQLAlchemy can resolve relationships.
import geneweb.core.models.Calendar_date  # noqa: F401
import geneweb.core.models.Person  # noqa: F401
import geneweb.core.models.Family  # noqa: F401
import geneweb.core.models.ChildInFamily  # noqa: F401

app = create_app()
client = TestClient(app)


def _make_db(base_dir, name):
    """Create a minimal SQLite DB with standard tables."""
    db_path = base_dir / f"{name}.db"
    con = sqlite3.connect(str(db_path))
    con.execute(
        "CREATE TABLE IF NOT EXISTS persons "
        "(id INTEGER PRIMARY KEY, "
        "first_name TEXT, last_name TEXT, "
        "gender TEXT, birth_date TEXT, "
        "death_date TEXT, birth_place TEXT, "
        "death_place TEXT, occupation TEXT, "
        "notes TEXT)"
    )
    con.execute(
        "CREATE TABLE IF NOT EXISTS families "
        "(id INTEGER PRIMARY KEY, "
        "spouse1_id INTEGER, spouse2_id INTEGER, "
        "marriage_date TEXT, marriage_place TEXT, "
        "divorce_date TEXT, notes TEXT)"
    )
    con.execute(
        "CREATE TABLE IF NOT EXISTS events "
        "(id INTEGER PRIMARY KEY, "
        "event_type TEXT, date TEXT, place TEXT, "
        "description TEXT, person_id INTEGER, "
        "family_id INTEGER, source_id INTEGER)"
    )
    con.execute(
        "CREATE TABLE IF NOT EXISTS notes "
        "(id INTEGER PRIMARY KEY, "
        "content TEXT, person_id INTEGER, "
        "event_id INTEGER)"
    )
    con.execute(
        "CREATE TABLE IF NOT EXISTS sources "
        "(id INTEGER PRIMARY KEY, "
        "title TEXT, reference TEXT, "
        "type TEXT, repository TEXT, "
        "notes TEXT)"
    )
    con.execute(
        "CREATE TABLE IF NOT EXISTS media "
        "(id INTEGER PRIMARY KEY, "
        "file_path TEXT, description TEXT, "
        "linked_person_id INTEGER, "
        "linked_event_id INTEGER)"
    )
    con.execute(
        "CREATE TABLE IF NOT EXISTS relations "
        "(id INTEGER PRIMARY KEY, "
        "person1_id INTEGER, "
        "person2_id INTEGER, "
        "relation_type TEXT, "
        "event_id INTEGER)"
    )
    con.execute(
        "CREATE TABLE IF NOT EXISTS "
        "children_in_family "
        "(id INTEGER PRIMARY KEY, "
        "person_id INTEGER, "
        "family_id INTEGER, "
        "relation_type TEXT)"
    )
    con.commit()
    con.close()
    return db_path


# -------------------------------------------------------
# bases.py — /api/bases
# -------------------------------------------------------


def test_list_bases_empty(monkeypatch, tmp_path):
    tmp_dir = tmp_path / "bases"
    tmp_dir.mkdir()
    monkeypatch.setattr(
        BaseManager,
        "bases_dir",
        staticmethod(lambda base_dir=None: tmp_dir),
    )
    r = client.get("/api/bases")
    assert r.status_code == 200
    assert r.json() == {"bases": []}


def test_create_base(monkeypatch, tmp_path):
    tmp_dir = tmp_path / "bases"
    tmp_dir.mkdir()
    monkeypatch.setattr(
        BaseManager,
        "bases_dir",
        staticmethod(lambda base_dir=None: tmp_dir),
    )
    r = client.post(
        "/api/bases",
        json={"name": "newbase"},
    )
    assert r.status_code == 201
    data = r.json()
    assert data["name"] == "newbase"
    assert (tmp_dir / "newbase.db").exists()


def test_create_duplicate(monkeypatch, tmp_path):
    tmp_dir = tmp_path / "bases"
    tmp_dir.mkdir()
    monkeypatch.setattr(
        BaseManager,
        "bases_dir",
        staticmethod(lambda base_dir=None: tmp_dir),
    )
    client.post(
        "/api/bases", json={"name": "dup"}
    )
    r = client.post(
        "/api/bases", json={"name": "dup"}
    )
    assert r.status_code == 409


def test_cleanup_base(monkeypatch, tmp_path):
    tmp_dir = tmp_path / "bases"
    tmp_dir.mkdir()
    monkeypatch.setattr(
        BaseManager,
        "bases_dir",
        staticmethod(lambda base_dir=None: tmp_dir),
    )
    _make_db(tmp_dir, "cleanme")
    r = client.post("/api/bases/cleanme/cleanup")
    assert r.status_code == 200
    assert r.json()["message"] == "cleaned"


def test_rename_base(monkeypatch, tmp_path):
    tmp_dir = tmp_path / "bases"
    tmp_dir.mkdir()
    monkeypatch.setattr(
        BaseManager,
        "bases_dir",
        staticmethod(lambda base_dir=None: tmp_dir),
    )
    _make_db(tmp_dir, "old")
    r = client.put(
        "/api/bases/old/rename",
        json={"new_name": "renamed"},
    )
    assert r.status_code == 200
    data = r.json()
    assert data["from"] == "old"
    assert data["to"] == "renamed"
    assert not (tmp_dir / "old.db").exists()
    assert (tmp_dir / "renamed.db").exists()


def test_delete_base(monkeypatch, tmp_path):
    tmp_dir = tmp_path / "bases"
    tmp_dir.mkdir()
    monkeypatch.setattr(
        BaseManager,
        "bases_dir",
        staticmethod(lambda base_dir=None: tmp_dir),
    )
    _make_db(tmp_dir, "todelete")
    r = client.delete("/api/bases/todelete")
    assert r.status_code == 204
    assert not (tmp_dir / "todelete.db").exists()


def test_delete_nonexistent(monkeypatch, tmp_path):
    tmp_dir = tmp_path / "bases"
    tmp_dir.mkdir()
    monkeypatch.setattr(
        BaseManager,
        "bases_dir",
        staticmethod(lambda base_dir=None: tmp_dir),
    )
    r = client.delete("/api/bases/nope")
    assert r.status_code == 404


# -------------------------------------------------------
# stats.py — /api/bases/{name}/stats
# -------------------------------------------------------


def test_stats(monkeypatch, tmp_path):
    tmp_dir = tmp_path / "bases"
    tmp_dir.mkdir()
    monkeypatch.setattr(
        BaseManager,
        "bases_dir",
        staticmethod(lambda base_dir=None: tmp_dir),
    )
    db_path = _make_db(tmp_dir, "statbase")
    con = sqlite3.connect(str(db_path))
    con.execute(
        "INSERT INTO persons "
        "(first_name, last_name) "
        "VALUES ('John', 'Doe')"
    )
    con.commit()
    con.close()
    r = client.get("/api/bases/statbase/stats")
    assert r.status_code == 200
    data = r.json()
    assert data["name"] == "statbase"
    assert data["counts"]["persons"] == 1


def test_stats_not_found(monkeypatch, tmp_path):
    tmp_dir = tmp_path / "bases"
    tmp_dir.mkdir()
    monkeypatch.setattr(
        BaseManager,
        "bases_dir",
        staticmethod(lambda base_dir=None: tmp_dir),
    )
    r = client.get("/api/bases/nope/stats")
    assert r.status_code == 404


# -------------------------------------------------------
# exports.py — /api/bases/{name}/export
# -------------------------------------------------------


def test_export_sqlite(monkeypatch, tmp_path):
    tmp_dir = tmp_path / "bases"
    tmp_dir.mkdir()
    monkeypatch.setattr(
        BaseManager,
        "bases_dir",
        staticmethod(lambda base_dir=None: tmp_dir),
    )
    _make_db(tmp_dir, "expdb")
    r = client.post(
        "/api/bases/expdb/export?format=sqlite"
    )
    assert r.status_code == 200
    assert len(r.content) > 0


def test_export_zip(monkeypatch, tmp_path):
    tmp_dir = tmp_path / "bases"
    tmp_dir.mkdir()
    monkeypatch.setattr(
        BaseManager,
        "bases_dir",
        staticmethod(lambda base_dir=None: tmp_dir),
    )
    _make_db(tmp_dir, "expzip")
    r = client.post(
        "/api/bases/expzip/export?format=zip"
    )
    assert r.status_code == 200
    assert len(r.content) > 0


def test_export_gedcom(monkeypatch, tmp_path):
    tmp_dir = tmp_path / "bases"
    tmp_dir.mkdir()
    monkeypatch.setattr(
        BaseManager,
        "bases_dir",
        staticmethod(lambda base_dir=None: tmp_dir),
    )
    _make_db(tmp_dir, "expged")
    r = client.post(
        "/api/bases/expged/export?format=gedcom"
    )
    assert r.status_code == 200
    text = r.text
    assert "HEAD" in text
    assert "TRLR" in text


def test_export_not_found(monkeypatch, tmp_path):
    tmp_dir = tmp_path / "bases"
    tmp_dir.mkdir()
    monkeypatch.setattr(
        BaseManager,
        "bases_dir",
        staticmethod(lambda base_dir=None: tmp_dir),
    )
    r = client.post(
        "/api/bases/nope/export?format=sqlite"
    )
    assert r.status_code == 404


# -------------------------------------------------------
# imports.py — /api/bases/import
# -------------------------------------------------------


def test_import_sqlite(monkeypatch, tmp_path):
    tmp_dir = tmp_path / "bases"
    tmp_dir.mkdir()
    monkeypatch.setattr(
        BaseManager,
        "bases_dir",
        staticmethod(lambda base_dir=None: tmp_dir),
    )
    src = _make_db(tmp_dir, "src_imp")
    with open(src, "rb") as f:
        content = f.read()
    src.unlink()
    buf = io.BytesIO(content)
    r = client.post(
        "/api/bases/import",
        data={"name": "imported", "format": "sqlite"},
        files={
            "file": (
                "imported.db",
                buf,
                "application/octet-stream",
            )
        },
    )
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_import_zip(monkeypatch, tmp_path):
    tmp_dir = tmp_path / "bases"
    tmp_dir.mkdir()
    monkeypatch.setattr(
        BaseManager,
        "bases_dir",
        staticmethod(lambda base_dir=None: tmp_dir),
    )
    src = _make_db(tmp_dir, "zipsrc")
    zip_buf = io.BytesIO()
    with ZipFile(zip_buf, "w", ZIP_DEFLATED) as z:
        z.write(str(src), arcname="zipsrc.db")
    src.unlink()
    zip_buf.seek(0)
    r = client.post(
        "/api/bases/import",
        data={"name": "fromzip", "format": "zip"},
        files={
            "file": (
                "archive.zip",
                zip_buf,
                "application/zip",
            )
        },
    )
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_import_gedcom(monkeypatch, tmp_path):
    tmp_dir = tmp_path / "bases"
    tmp_dir.mkdir()
    monkeypatch.setattr(
        BaseManager,
        "bases_dir",
        staticmethod(lambda base_dir=None: tmp_dir),
    )
    gedcom = (
        "0 HEAD\n"
        "1 SOUR TEST\n"
        "1 GEDC\n"
        "2 VERS 5.5.1\n"
        "0 @I1@ INDI\n"
        "1 NAME John /Doe/\n"
        "1 SEX M\n"
        "0 TRLR\n"
    )
    buf = io.BytesIO(gedcom.encode("utf-8"))
    r = client.post(
        "/api/bases/import",
        data={
            "name": "fromged",
            "format": "gedcom",
        },
        files={
            "file": (
                "test.ged",
                buf,
                "text/plain",
            )
        },
    )
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "ok"
    assert data["persons"] >= 1


# -------------------------------------------------------
# backup.py — /api/bases/{name}/backup + /restore
# -------------------------------------------------------


def test_backup(monkeypatch, tmp_path):
    tmp_dir = tmp_path / "bases"
    tmp_dir.mkdir()
    monkeypatch.setattr(
        BaseManager,
        "bases_dir",
        staticmethod(lambda base_dir=None: tmp_dir),
    )
    _make_db(tmp_dir, "bkbase")
    r = client.post("/api/bases/bkbase/backup")
    assert r.status_code == 200
    assert len(r.content) > 0


def test_restore(monkeypatch, tmp_path):
    tmp_dir = tmp_path / "bases"
    tmp_dir.mkdir()
    monkeypatch.setattr(
        BaseManager,
        "bases_dir",
        staticmethod(lambda base_dir=None: tmp_dir),
    )
    src = _make_db(tmp_dir, "rsrc")
    zip_buf = io.BytesIO()
    with ZipFile(zip_buf, "w", ZIP_DEFLATED) as z:
        z.write(str(src), arcname="rsrc.db")
    src.unlink()
    zip_buf.seek(0)
    r = client.post(
        "/api/bases/restore",
        data={"target_name": "restored"},
        files={
            "file": (
                "backup.zip",
                zip_buf,
                "application/zip",
            )
        },
    )
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


# -------------------------------------------------------
# merge.py — /api/bases/merge
# -------------------------------------------------------


def test_merge(monkeypatch, tmp_path):
    tmp_dir = tmp_path / "bases"
    tmp_dir.mkdir()
    monkeypatch.setattr(
        BaseManager,
        "bases_dir",
        staticmethod(lambda base_dir=None: tmp_dir),
    )
    _make_db(tmp_dir, "a")
    _make_db(tmp_dir, "b")
    r = client.post(
        "/api/bases/merge"
        "?base_a=a&base_b=b&target=c"
    )
    assert r.status_code == 200
    assert (tmp_dir / "c.db").exists()


def test_merge_same(monkeypatch, tmp_path):
    tmp_dir = tmp_path / "bases"
    tmp_dir.mkdir()
    monkeypatch.setattr(
        BaseManager,
        "bases_dir",
        staticmethod(lambda base_dir=None: tmp_dir),
    )
    _make_db(tmp_dir, "a")
    r = client.post(
        "/api/bases/merge"
        "?base_a=a&base_b=a&target=c"
    )
    assert r.status_code == 400


# -------------------------------------------------------
# Additional error paths
# -------------------------------------------------------


def test_cleanup_not_found(monkeypatch, tmp_path):
    tmp_dir = tmp_path / "bases"
    tmp_dir.mkdir()
    monkeypatch.setattr(
        BaseManager,
        "bases_dir",
        staticmethod(lambda base_dir=None: tmp_dir),
    )
    r = client.post("/api/bases/nope/cleanup")
    assert r.status_code == 404


def test_rename_not_found(monkeypatch, tmp_path):
    tmp_dir = tmp_path / "bases"
    tmp_dir.mkdir()
    monkeypatch.setattr(
        BaseManager,
        "bases_dir",
        staticmethod(lambda base_dir=None: tmp_dir),
    )
    r = client.put(
        "/api/bases/nope/rename",
        json={"new_name": "new"},
    )
    assert r.status_code == 404


def test_rename_target_exists(
    monkeypatch, tmp_path
):
    tmp_dir = tmp_path / "bases"
    tmp_dir.mkdir()
    monkeypatch.setattr(
        BaseManager,
        "bases_dir",
        staticmethod(lambda base_dir=None: tmp_dir),
    )
    _make_db(tmp_dir, "src")
    _make_db(tmp_dir, "dst")
    r = client.put(
        "/api/bases/src/rename",
        json={"new_name": "dst"},
    )
    assert r.status_code == 409


def test_create_base_invalid_name(
    monkeypatch, tmp_path
):
    tmp_dir = tmp_path / "bases"
    tmp_dir.mkdir()
    monkeypatch.setattr(
        BaseManager,
        "bases_dir",
        staticmethod(lambda base_dir=None: tmp_dir),
    )
    r = client.post(
        "/api/bases",
        json={"name": "bad name!"},
    )
    assert r.status_code == 422


def test_merge_not_found(monkeypatch, tmp_path):
    tmp_dir = tmp_path / "bases"
    tmp_dir.mkdir()
    monkeypatch.setattr(
        BaseManager,
        "bases_dir",
        staticmethod(lambda base_dir=None: tmp_dir),
    )
    r = client.post(
        "/api/bases/merge"
        "?base_a=nope1&base_b=nope2&target=c"
    )
    assert r.status_code == 404


def test_merge_target_exists(
    monkeypatch, tmp_path
):
    tmp_dir = tmp_path / "bases"
    tmp_dir.mkdir()
    monkeypatch.setattr(
        BaseManager,
        "bases_dir",
        staticmethod(lambda base_dir=None: tmp_dir),
    )
    _make_db(tmp_dir, "m1")
    _make_db(tmp_dir, "m2")
    _make_db(tmp_dir, "existing")
    r = client.post(
        "/api/bases/merge"
        "?base_a=m1&base_b=m2&target=existing"
    )
    assert r.status_code == 409


# -------------------------------------------------------
# create_bases_empty
# -------------------------------------------------------


def test_create_base_empty_page(
    monkeypatch, tmp_path
):
    monkeypatch.setattr(
        BaseManager,
        "bases_dir",
        staticmethod(
            lambda base_dir=None: tmp_path
        ),
    )
    r = client.get("/create_base_empty")
    assert r.status_code == 200
    ct = r.headers["content-type"]
    assert "text/html" in ct


def test_create_base_empty_post(
    monkeypatch, tmp_path
):
    monkeypatch.setattr(
        BaseManager,
        "bases_dir",
        staticmethod(
            lambda base_dir=None: tmp_path
        ),
    )
    r = client.post(
        "/create_base",
        data={"base_name": "emptytest"},
    )
    assert r.status_code == 200
    data = r.json()
    assert "message" in data or "error" in data


# -------------------------------------------------------
# set_language (via admin app)
# -------------------------------------------------------

def test_admin_index(monkeypatch, tmp_path):
    monkeypatch.setattr(
        BaseManager,
        "bases_dir",
        staticmethod(
            lambda base_dir=None: tmp_path
        ),
    )
    monkeypatch.setattr(
        BaseManager,
        "list_bases",
        classmethod(lambda cls, bd=None: []),
    )
    r = client.get("/")
    assert r.status_code == 200
    ct = r.headers["content-type"]
    assert "text/html" in ct

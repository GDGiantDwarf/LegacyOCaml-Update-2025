from conftest import db
from geneweb.core.database import Database

def test_if_base_exist(tmp_path, monkeypatch):
    monkeypatch.setattr(Database, "BASES_FOLDER", tmp_path)

    base_name = "alpha"

    (tmp_path / f"{base_name}.db").touch()

    results = Database.is_base_exist(base_name)
    assert results == True

def test_if_base_not_exist(tmp_path, monkeypatch):
    monkeypatch.setattr(Database, "BASES_FOLDER", tmp_path)

    base_name = "alpha"

    (tmp_path / f"{base_name}.db").touch()

    results = Database.is_base_exist("fake base")
    assert results == False
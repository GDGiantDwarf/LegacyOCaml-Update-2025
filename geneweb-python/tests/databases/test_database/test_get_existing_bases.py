from conftest import db
from geneweb.core.database import Database

def test_list_existings_bases(tmp_path, monkeypatch):
    monkeypatch.setattr(Database, "BASES_FOLDER", tmp_path)

    (tmp_path / "alpha.db").touch()
    (tmp_path / "beta.db").touch()

    results = Database.get_existing_bases()

    assert "alpha" in results
    assert "beta" in results
    assert len(results) == 2
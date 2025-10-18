import os
import tempfile
import pytest
from fastapi.testclient import TestClient
from geneweb.web.admin.server import create_app


@pytest.fixture(scope="module")
def client():
    app = create_app()
    return TestClient(app)


def test_stats_empty_base(tmp_path, client):
    base_dir = tmp_path / "bases"
    base_dir.mkdir()
    (base_dir / "alpha.db").touch()

    response = client.get("/api/bases/alpha/stats")
    assert response.status_code == 200
    data = response.json()

    assert data["name"] == "alpha"
    assert "size_bytes" in data
    assert isinstance(data["counts"], dict)
    assert all(isinstance(v, int) for v in data["counts"].values())


def test_import_and_export(client, tmp_path):
    db_file = tmp_path / "alpha.db"
    db_file.write_text("")
    files = {"file": ("alpha.db", open(db_file, "rb"), "application/octet-stream")}
    resp = client.post("/api/bases/import", data={"name": "beta", "format": "sqlite"}, files=files)
    assert resp.status_code in (200, 201)
    assert "beta" in resp.text

    resp = client.post("/api/bases/alpha/export?format=sqlite")
    assert resp.status_code == 200


def test_backup_and_restore(client):
    resp = client.post("/api/bases/alpha/backup")
    assert resp.status_code == 200

    tmpfile = tempfile.NamedTemporaryFile(suffix=".zip")
    files = {"file": (os.path.basename(tmpfile.name), tmpfile, "application/zip")}
    resp = client.post("/api/bases/restore", files=files)
    assert resp.status_code == 200


def test_merge_stub(client):
    resp = client.post("/api/bases/merge?base_a=alpha&base_b=beta&target=gamma")
    assert resp.status_code == 501

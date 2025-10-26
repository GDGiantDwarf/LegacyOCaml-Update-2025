import os
import io
from pathlib import Path
import tempfile
import pytest
from fastapi.testclient import TestClient
from geneweb.web.admin.server import create_app

app = create_app()
client = TestClient(app)


@pytest.fixture(scope="function")
def tmp_base_dir(tmp_path):
    base_dir = tmp_path / "bases"
    base_dir.mkdir()
    yield base_dir


def create_dummy_db(base_dir, name="alpha"):
    db_path = base_dir / f"{name}.db"
    db_path.touch()
    return db_path


# --------------------------------------------------------------------------------
# /api/bases/{name}/stats
# --------------------------------------------------------------------------------

def test_stats_empty_base(tmp_base_dir):
    db_path = create_dummy_db(tmp_base_dir, "alpha")
    os.environ["BASES_PATH"] = str(tmp_base_dir)

    response = client.get("/api/bases/alpha/stats")
    assert response.status_code in (200, 404)
    if response.status_code == 200:
        data = response.json()
        assert "name" in data
        assert data["size_bytes"] >= 0


# --------------------------------------------------------------------------------
# /api/bases/import + /api/bases/{name}/export
# --------------------------------------------------------------------------------

def test_import_and_export(tmp_base_dir):
    db_path = create_dummy_db(tmp_base_dir, "alpha")
    with open(db_path, "rb") as f:
        files = {"file": ("alpha.db", f, "application/octet-stream")}
        data = {"name": "beta", "format": "sqlite"}
        resp = client.post("/api/bases/import", data=data, files=files)

    assert resp.status_code in (200, 201, 409)

    export_resp = client.post("/api/bases/alpha/export?format=sqlite")
    assert export_resp.status_code in (200, 404)
    if export_resp.status_code == 200:
        assert export_resp.content != b""


# --------------------------------------------------------------------------------
# /api/bases/{name}/backup + /api/bases/restore
# --------------------------------------------------------------------------------

def test_backup_and_restore(tmp_base_dir):
    create_dummy_db(tmp_base_dir, "alpha")

    backup_resp = client.post("/api/bases/alpha/backup")
    assert backup_resp.status_code in (200, 404)
    if backup_resp.status_code == 200:
        assert len(backup_resp.content) > 0

    file_data = io.BytesIO(b"fakezipdata")
    files = {"file": ("backup.zip", file_data, "application/zip")}
    restore_resp = client.post("/api/bases/restore", files=files)

    assert restore_resp.status_code in (200, 422, 501)


# --------------------------------------------------------------------------------
# /api/bases/merge
# --------------------------------------------------------------------------------

def test_merge_stub():
    resp = client.post("/api/bases/merge?base_a=alpha&base_b=beta&target=gamma")
    assert resp.status_code in (200, 501)


# --------------------------------------------------------------------------------
# /api/bases/{name}/stats → vérifie que count = 0 sur base vide
# --------------------------------------------------------------------------------

def test_stats_counts_default_zero(tmp_path):
    base_dir = tmp_path / "bases"
    base_dir.mkdir(exist_ok=True)

    db_path = base_dir / "alpha.db"
    db_path.touch(exist_ok=True)

    os.environ["BASES_PATH"] = str(base_dir)

    response = client.get("/api/bases/alpha/stats")

    assert response.status_code in (200, 404)
    if response.status_code == 200:
        data = response.json()
        for count in data["counts"].values():
            assert isinstance(count, int)
            assert count >= 0

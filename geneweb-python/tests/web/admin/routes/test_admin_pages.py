from fastapi.testclient import TestClient
from geneweb.web.admin.server import create_app
from geneweb.core.database import BaseManager

app = create_app()
client = TestClient(app)


def test_welcome(monkeypatch, tmp_path):
    monkeypatch.setattr(
        BaseManager,
        "bases_dir",
        staticmethod(lambda bd=None: tmp_path),
    )
    monkeypatch.setattr(
        BaseManager,
        "list_bases",
        classmethod(lambda cls, bd=None: []),
    )
    r = client.get("/welcome")
    assert r.status_code == 200
    assert "text/html" in r.headers["content-type"]


def test_cleanup_page(monkeypatch, tmp_path):
    monkeypatch.setattr(
        BaseManager,
        "bases_dir",
        staticmethod(lambda bd=None: tmp_path),
    )
    monkeypatch.setattr(
        BaseManager,
        "list_bases",
        classmethod(lambda cls, bd=None: []),
    )
    r = client.get("/cleanup")
    assert r.status_code == 200
    assert "text/html" in r.headers["content-type"]


def test_rename_page(monkeypatch, tmp_path):
    monkeypatch.setattr(
        BaseManager,
        "bases_dir",
        staticmethod(lambda bd=None: tmp_path),
    )
    monkeypatch.setattr(
        BaseManager,
        "list_bases",
        classmethod(lambda cls, bd=None: []),
    )
    r = client.get("/rename")
    assert r.status_code == 200
    assert "text/html" in r.headers["content-type"]


def test_delete_page(monkeypatch, tmp_path):
    monkeypatch.setattr(
        BaseManager,
        "bases_dir",
        staticmethod(lambda bd=None: tmp_path),
    )
    monkeypatch.setattr(
        BaseManager,
        "list_bases",
        classmethod(lambda cls, bd=None: []),
    )
    r = client.get("/delete")
    assert r.status_code == 200
    assert "text/html" in r.headers["content-type"]


def test_merge_page(monkeypatch, tmp_path):
    monkeypatch.setattr(
        BaseManager,
        "bases_dir",
        staticmethod(lambda bd=None: tmp_path),
    )
    monkeypatch.setattr(
        BaseManager,
        "list_bases",
        classmethod(lambda cls, bd=None: []),
    )
    r = client.get("/merge-page")
    assert r.status_code == 200
    assert "text/html" in r.headers["content-type"]


def test_list_page(monkeypatch, tmp_path):
    monkeypatch.setattr(
        BaseManager,
        "bases_dir",
        staticmethod(lambda bd=None: tmp_path),
    )
    monkeypatch.setattr(
        BaseManager,
        "list_bases",
        classmethod(lambda cls, bd=None: []),
    )
    r = client.get("/list")
    assert r.status_code == 200
    assert "text/html" in r.headers["content-type"]

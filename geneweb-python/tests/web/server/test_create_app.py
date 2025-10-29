import types
from fastapi import FastAPI
from fastapi.routing import APIRoute
from pathlib import Path
import pytest

from geneweb.web.server.server import create_app
from geneweb.web.utils import BASE_DIR


def test_create_app_returns_fastapi_instance():
    app = create_app()
    assert isinstance(app, FastAPI)
    assert "GeneWeb Public" in app.title


def test_create_app_mounts_static_dir(tmp_path, monkeypatch):
    static_dir = tmp_path / "server/static"
    static_dir.mkdir(parents=True)
    monkeypatch.setattr("geneweb.web.utils.BASE_DIR", tmp_path)

    app = create_app()

    mounts = [r for r in app.routes if getattr(r, "path", None) == "/static"]
    assert mounts, "Le répertoire /static devrait être monté"
    assert mounts[0].name == "static"

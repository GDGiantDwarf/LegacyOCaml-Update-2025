"""Tests for the public server index routes."""

import html

import pytest
from fastapi.testclient import TestClient

from geneweb.web.server.server import create_app


@pytest.fixture()
def client():
    """Create a fresh TestClient for each test."""
    app = create_app()
    return TestClient(app)


def test_index_page_renders_html(client):
    """GET / should return 200 with HTML content."""
    response = client.get("/")
    assert response.status_code == 200
    content_type = response.headers["content-type"]
    assert "text/html" in content_type


def test_select_base_redirects_if_valid(
    client, monkeypatch
):
    """POST /select-base/{name} redirects when valid."""
    monkeypatch.setattr(
        "geneweb.web.server.routes.index"
        ".BaseManager.list_bases",
        lambda base_dir=None: ["test_base"],
    )
    response = client.post(
        "/select-base/test_base",
        follow_redirects=False,
    )
    assert response.status_code == 303
    location = response.headers["location"]
    assert location == "/base/test_base"


def test_select_base_shows_error_if_invalid(
    client, monkeypatch
):
    """POST /select-base/{name} shows error if missing."""
    monkeypatch.setattr(
        "geneweb.web.server.routes.index"
        ".BaseManager.list_bases",
        lambda base_dir=None: [],
    )
    response = client.post("/select-base/fake")
    assert response.status_code == 200
    decoded = html.unescape(response.text)
    assert "n'existe pas" in decoded

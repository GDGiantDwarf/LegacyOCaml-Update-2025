"""Tests for the public server translations API."""

import pytest
from fastapi.testclient import TestClient

from geneweb.web.server.server import create_app


@pytest.fixture()
def client():
    """Create a fresh TestClient."""
    app = create_app()
    return TestClient(app)


def test_translations_en(client):
    """GET /api/translations?lang=en returns JSON."""
    response = client.get(
        "/api/translations?lang=en"
    )
    assert response.status_code == 200
    body = response.json()
    assert isinstance(body, dict)


def test_translations_unknown(client):
    """GET /api/translations?lang=xx returns fallback."""
    response = client.get(
        "/api/translations?lang=xx"
    )
    assert response.status_code == 200
    body = response.json()
    assert isinstance(body, dict)

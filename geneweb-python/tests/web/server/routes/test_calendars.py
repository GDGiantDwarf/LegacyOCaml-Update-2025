"""Tests for the public server calendar routes."""

import pytest
from fastapi.testclient import TestClient

from geneweb.web.server.server import create_app


@pytest.fixture()
def client():
    """Create a fresh TestClient."""
    app = create_app()
    return TestClient(app)


def test_calendars_page(client):
    """GET /calendars returns 200 with HTML content."""
    response = client.get("/calendars")
    assert response.status_code == 200
    content_type = response.headers["content-type"]
    assert "text/html" in content_type


def test_convert_date(client):
    """POST /api/convert-date returns JSON conversions."""
    form_data = {
        "year": "2000",
        "month": "1",
        "day": "1",
    }
    response = client.post(
        "/api/convert-date", data=form_data
    )
    assert response.status_code == 200
    body = response.json()
    assert "gregorian" in body
    assert "julian" in body
    assert "french_republican" in body
    assert "hebrew" in body


def test_set_language(client):
    """POST /set-language sets session lang."""
    r = client.post(
        "/set-language",
        data={"lang": "fr"},
        follow_redirects=False,
    )
    assert r.status_code == 303

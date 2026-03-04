import pytest
from fastapi.testclient import TestClient
from geneweb.web.admin.server import create_app

app = create_app()
client = TestClient(app)


def test_index_page_renders_html():
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]

    text = response.text
    assert (
        "geneweb" in text.lower()
        or "admin" in text.lower()
        or "Dashboard" in text
    ), (
        "Expected admin content in response: "
        f"{text[:200]}"
    )

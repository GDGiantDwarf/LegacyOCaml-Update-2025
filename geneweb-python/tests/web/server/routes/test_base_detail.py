import pytest
from fastapi.testclient import TestClient
from geneweb.web.server.server import create_app

app = create_app()
client = TestClient(app)


def test_base_detail_page_renders_html():
    base_name = "base-teste"

    response = client.get(f"/base/{base_name}")
    assert response.status_code == 200
    content_type = response.headers["content-type"]
    assert content_type.startswith("text/html")
    assert base_name in response.text

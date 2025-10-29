import pytest
import html
from fastapi.testclient import TestClient
from geneweb.web.server.routes.base_detail import router
from fastapi import FastAPI

app = FastAPI()
app.include_router(router)

client = TestClient(app)


def test_base_detail_page_renders_html():
    base_name = "base-teste"

    response = client.get(f"/base/{base_name}")
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/html")
    assert base_name in response.text

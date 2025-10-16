import pytest
import html
from fastapi.testclient import TestClient
from geneweb.web.admin.routes.index import router
from fastapi import FastAPI

app = FastAPI()
app.include_router(router)

client = TestClient(app)

def test_index_page_renders_html():
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "Panneau d&#39;administration" in response.text
import pytest
import html
from fastapi.testclient import TestClient
from geneweb.web.server.routes.index import router
from fastapi import FastAPI


app = FastAPI()
app.include_router(router)

client = TestClient(app)

"""
def test_index_page_renders_html():
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "GeneWeb" in response.text

def test_select_base_redirects_if_valid(monkeypatch):
    monkeypatch.setattr("geneweb.web.server.routes.index.\
    Database.is_base_exist", lambda name: True)

    base_name = "famille_dupont"

    response = client.post("/select-base", data={"base_name": \
    base_name}, follow_redirects=False)
    assert response.status_code == 303
    assert response.headers["location"] == f"/base/{base_name}"

def test_select_base_redirects_if_not_valid(monkeypatch):
    monkeypatch.setattr("geneweb.web.server.routes.\
    index.Database.is_base_exist", lambda name: False)

    base_name = "base name fake"

    response = client.post("/select-base", data={"base_name": base_name})
    decoded = html.unescape(response.text)

    assert response.status_code == 200
    assert f"La base '{base_name}' n'existe pas" in decoded
"""

# geneweb/web/server.py
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
import pathlib
from ..core.repositories.person_repository import PersonRepository

def create_app(base_dir="bases", lang="fr"):
    """Crée une instance configurée de l’application GeneWeb."""
    app = FastAPI(title=f"GeneWeb Python — {lang.upper()}")

    BASE_DIR = pathlib.Path(__file__).parent
    templates = Jinja2Templates(directory=str(BASE_DIR / "templates/server"))

    static_dir = BASE_DIR / "static"
    if static_dir.exists():
        app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

    # --- ROUTES ---
    @app.get("/", response_class=HTMLResponse)
    async def index(request: Request):
        context = {
            "request": request,
            "site_title": "GeneWeb-Python — Demo",
            "bases": [
                {"name": "base-test", "persons": 1234, "last_import": "2025-10-03"},
                {"name": "demo-family", "persons": 42, "last_import": "2024-12-12"},
            ],
        }
        return templates.TemplateResponse("index.html", context)

    @app.get("/base-test", response_class=HTMLResponse)
    async def base_detail(request: Request):
        context = {"request": request}
        return templates.TemplateResponse("handle-bases.html", context)

    return app

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
import pathlib

def create_app(base_dir="bases", lang="fr"):
    """Crée une instance configurée de l’application GeneWeb."""
    app = FastAPI(title="Mini GeneWeb (demo)")

    # Templates : le dossier 'templates' (relatif au fichier main.py)
    BASE_DIR = pathlib.Path(__file__).parent
    templates = Jinja2Templates(directory=str(BASE_DIR / "templates/admin_server"))

    # Optionnel : servir un répertoire static (css/js/images) si tu en ajoutes
    static_dir = BASE_DIR / "static"
    if static_dir.exists():
        app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

    @app.get("/", response_class=HTMLResponse)
    async def index(request: Request):
        # Exemple de données que tu pourrais transmettre (résumé d'une base)
        context = {
            "request": request,
            "site_title": "GeneWeb-admin-Python — Demo",
            "bases": [
                {"name": "base-test", "persons": 1234, "last_import": "2025-10-03"},
                {"name": "demo-family", "persons": 42, "last_import": "2024-12-12"},
            ],
        }
        return templates.TemplateResponse("index.html", context)
    
    return app
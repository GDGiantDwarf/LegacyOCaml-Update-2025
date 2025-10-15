from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from geneweb.web.utils import BASE_DIR
from .routes import index

def create_app(base_dir="bases", lang="fr"):
    """Crée et configure le serveur d'administration GeneWeb."""
    app = FastAPI(title="GeneWeb Admin")

    static_dir = BASE_DIR / "admin/static"
    if static_dir.exists():
        app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

    # Routes
    app.include_router(index.router)

    return app

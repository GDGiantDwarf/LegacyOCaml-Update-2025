from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path

from geneweb.web.admin.routes import index, bases


def create_app(base_dir: str | None = None, lang: str | None = None) -> FastAPI:
    """
    Application FastAPI pour le module d'administration (gwsetup).
    Permet de gérer les bases : création, suppression, renommage, nettoyage.
    """
    app = FastAPI(
        title="GeneWeb Admin (gwsetup)",
        description="Interface d'administration pour la gestion des bases GeneWeb",
        version="0.1",
    )

    # Dossiers statiques et templates
    base_path = Path(__file__).resolve().parent
    static_dir = base_path / "static"
    templates_dir = base_path / "templates"

    if static_dir.exists():
        app.mount("/static", StaticFiles(directory=static_dir), name="static")

    if templates_dir.exists():
        Jinja2Templates(directory=templates_dir)

    # Routes
    app.include_router(index.router)
    app.include_router(bases.router, prefix="/api/bases", tags=["bases"])

    return app


# --- Entry point utilisé par geneweb/gwsetup.py ---
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(create_app(), host="0.0.0.0", port=2316)

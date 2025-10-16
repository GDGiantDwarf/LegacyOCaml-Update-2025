from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from geneweb.web.utils import BASE_DIR
from .routes import index, base_detail, calendars

def create_app(base_dir="bases", lang="fr"):
    """Crée et configure le serveur principal GeneWeb."""
    app = FastAPI(title=f"GeneWeb Public — {lang.upper()}")

    static_dir = BASE_DIR / "server/static"
    if static_dir.exists():
        app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

    # Routes
    app.include_router(index.router)
    app.include_router(base_detail.router)
    app.include_router(calendars.router)
    
    return app

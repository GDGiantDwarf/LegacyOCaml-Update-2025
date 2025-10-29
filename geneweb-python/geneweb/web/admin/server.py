from geneweb.web.admin.routes import (
    index,
    bases,
    stats,
    exports,
    imports,
    backup,
    merge,
    create_bases_empty,
)
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from pathlib import Path
from geneweb.web.utils import BASE_DIR
from geneweb.core.services.language_manager import LanguageManager
from geneweb.core.services.template_config import ExtendedJinja2Templates


IS_START = True


def create_app(base_dir: str | None = None,
               lang: str | None = None) -> FastAPI:
    app = FastAPI(
        title="GeneWeb Admin (gwsetup)",
        description=(
            "Interface d'administration pour la gestion des bases GeneWeb"
        ),
        version="0.1.0",
    )

    # --- Initialisation de la langue ---
    lang_manager = LanguageManager(BASE_DIR, lang)
    templates = ExtendedJinja2Templates(
        directory=str(BASE_DIR / "admin/templates"), lang_manager=lang_manager
    )
    app.state.lang_manager = lang_manager
    app.state.templates = templates

    @app.middleware("http")
    async def language_middleware(request: Request, call_next):
        global IS_START
        lang1 = ""

        if IS_START:
            lang1 = lang
            IS_START = False
        else:
            lang1 = request.session.get(
                "lang", getattr(
                    request.state, "lang", lang))

        request.state.lang = lang1
        request.state.t = lambda key: request.app.state.lang_manager.get_text(
            key, lang1
        )

        response = await call_next(request)
        return response

    static_dir = BASE_DIR / "admin/static"
    if static_dir.exists():
        app.mount(
            "/static",
            StaticFiles(
                directory=str(static_dir)),
            name="static")

    """
    # --- Dossiers statiques et templates ---
    base_path = Path(__file__).resolve().parent
    static_dir = base_path / "static"
    templates_dir = base_path / "templates"

    if static_dir.exists():
        app.mount("/static", StaticFiles(directory=static_dir), name="static")
    """

    # --- Routes principales ---
    app.include_router(index.router)
    app.include_router(bases.router, prefix="/api/bases", tags=["bases"])

    # --- Routes additionnelles (nouveaux endpoints admin) ---
    app.include_router(stats.router)
    app.include_router(exports.router)
    app.include_router(imports.router)
    app.include_router(backup.router)
    app.include_router(merge.router)
    app.include_router(create_bases_empty.router)

    app.add_middleware(SessionMiddleware, secret_key="secret")

    return app

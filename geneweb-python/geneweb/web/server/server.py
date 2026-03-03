from fastapi import FastAPI, Request, Form
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

from geneweb.web.utils import BASE_DIR
from .routes import (
    index,
    base_actions,
    base_data,
    base_info,
    set_language,
    calendars,
    translations_api,
)
from geneweb.core.services.language_manager import (
    LanguageManager,
)
from geneweb.core.services.template_config import (
    ExtendedJinja2Templates,
)

IS_START = True


def create_app(base_dir="bases", lang="en"):
    app = FastAPI(title=f"GeneWeb Public — {lang.upper()}")

    # --- Initialisation de la langue ---
    lang_manager = LanguageManager(BASE_DIR, lang)
    templates = ExtendedJinja2Templates(
        directory=str(BASE_DIR / "server/templates"), lang_manager=lang_manager
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

    shared_static = BASE_DIR / "shared_static"
    if shared_static.exists():
        app.mount(
            "/static",
            StaticFiles(
                directory=str(shared_static)),
            name="static")

    app.include_router(index.router)
    app.include_router(base_actions.router)
    app.include_router(base_data.router)
    app.include_router(base_info.router)
    app.include_router(set_language.router)
    app.include_router(calendars.router)
    app.include_router(translations_api.router)

    app.add_middleware(SessionMiddleware, secret_key="secret")

    return app

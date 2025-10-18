from fastapi import FastAPI, Request, Form
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import RedirectResponse

from geneweb.web.utils import BASE_DIR
from .routes import index, base_detail, set_language
from geneweb.core.services.language_manager import LanguageManager
from geneweb.core.services.template_config import ExtendedJinja2Templates

IS_START = True
from .routes import index, base_detail, calendars

def create_app(base_dir="bases", lang="en"):
    app = FastAPI(title=f"GeneWeb Public — {lang.upper()}")

    # --- Initialisation de la langue ---
    lang_manager = LanguageManager(BASE_DIR, lang)
    templates = ExtendedJinja2Templates(directory=str(BASE_DIR /  "server/templates"), lang_manager=lang_manager)
    app.state.lang_manager = lang_manager
    app.state.templates = templates

    @app.middleware("http")
    async def language_middleware(request: Request, call_next):
        global IS_START
        lang1 = ""

        if (IS_START):
            lang1 = lang
            IS_START = False
        else:
            lang1 = request.session.get("lang", getattr(request.state, "lang", lang))

        request.state.lang = lang1
        request.state.t = lambda key: request.app.state.lang_manager.get_text(key, lang1)

        response = await call_next(request)
        return response

    static_dir = BASE_DIR / "server/static"
    if static_dir.exists():
        app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

    app.include_router(index.router)
    app.include_router(base_detail.router)
    app.include_router(set_language.router)

    app.add_middleware(SessionMiddleware, secret_key="secret")
    return app
    app.include_router(calendars.router)
    
    return app

import json

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse

from geneweb.core.database import BaseManager

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    base_dir = getattr(request.app.state, "base_dir", None)
    bases = BaseManager.list_bases(base_dir)
    templates = request.app.state.templates
    lang_manager = request.app.state.lang_manager
    lang = getattr(
        request.state,
        "lang",
        lang_manager.default_lang,
    )

    translations = (
        lang_manager.get_translations_for_lang(lang)
    )
    translations_json = json.dumps(
        translations, ensure_ascii=False
    )

    context = templates.get_context(request)
    context.update(
        {
            "list_bases": bases,
            "translations_json": translations_json,
            "lang": lang,
        }
    )
    return templates.TemplateResponse(
        request, "index.html", context
    )


@router.post("/select-base/{base_name}")
async def select_base(
    request: Request, base_name: str
):
    base_dir = getattr(
        request.app.state, "base_dir", None
    )
    existing = BaseManager.list_bases(base_dir)
    if base_name not in existing:
        templates = request.app.state.templates
        lang_manager = request.app.state.lang_manager
        lang = getattr(
            request.state,
            "lang",
            lang_manager.default_lang,
        )

        translations = (
            lang_manager.get_translations_for_lang(
                lang
            )
        )
        translations_json = json.dumps(
            translations, ensure_ascii=False
        )

        context = templates.get_context(request)
        context.update(
            {
                "list_bases": existing,
                "translations_json": translations_json,
                "lang": lang,
                "error_message": (
                    f"La base '{base_name}' "
                    f"n'existe pas"
                ),
            }
        )
        return templates.TemplateResponse(
            request, "index.html", context
        )

    return RedirectResponse(
        url=f"/base/{base_name}", status_code=303
    )

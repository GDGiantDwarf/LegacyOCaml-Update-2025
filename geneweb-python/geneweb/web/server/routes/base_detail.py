import json
import sqlite3

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from geneweb.core.database import Database

router = APIRouter()


def _get_person_count(base_name: str) -> int:
    """Return the number of persons in the base."""
    db_path = Database.BASES_FOLDER / f"{base_name}.db"
    if not db_path.exists():
        return 0
    try:
        con = sqlite3.connect(str(db_path))
        cur = con.execute(
            "SELECT COUNT(*) FROM persons"
        )
        count = cur.fetchone()[0]
        con.close()
        return count
    except Exception:
        return 0


@router.get(
    "/base/{base_name}", response_class=HTMLResponse
)
async def base_detail(
    request: Request, base_name: str
):
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
    person_count = _get_person_count(base_name)

    context = templates.get_context(request)
    context.update(
        {
            "base_name": base_name,
            "person_count": person_count,
            "translations_json": translations_json,
            "lang": lang,
        }
    )
    return templates.TemplateResponse(
        request, "base_details.html", context
    )

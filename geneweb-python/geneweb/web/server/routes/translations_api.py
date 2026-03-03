from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

router = APIRouter()


@router.get("/api/translations")
async def get_translations(
    request: Request, lang: str = "en"
) -> JSONResponse:
    lang_manager = request.app.state.lang_manager
    translations = (
        lang_manager.get_translations_for_lang(lang)
    )
    return JSONResponse(content=translations)

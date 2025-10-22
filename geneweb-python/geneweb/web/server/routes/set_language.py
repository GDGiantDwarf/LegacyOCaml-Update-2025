from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from starlette.templating import Jinja2Templates
from geneweb.web.utils import BASE_DIR
from geneweb.core.database import Database

#templates = Jinja2Templates(directory=str(BASE_DIR / "server/templates"))
router = APIRouter()

@router.post("/set-language")
async def set_language(request: Request, lang: str = Form(...)):
    request.session["lang"] = lang
    # Redirige vers la page précédente ou /
    print(request.session["lang"])
    return RedirectResponse(url=request.headers.get("referer", "/"), status_code=303)
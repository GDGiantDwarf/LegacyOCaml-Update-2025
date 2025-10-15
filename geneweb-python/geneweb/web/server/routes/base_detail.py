from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from starlette.templating import Jinja2Templates
from geneweb.web.utils import BASE_DIR

templates = Jinja2Templates(directory=str(BASE_DIR / "server/templates"))
router = APIRouter()

@router.get("/base-test", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(
        "handle-bases.html",
        {"request": request, "title": "GeneWeb - Accueil"}
    )

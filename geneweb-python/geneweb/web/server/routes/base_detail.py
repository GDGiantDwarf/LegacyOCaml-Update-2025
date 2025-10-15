from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from starlette.templating import Jinja2Templates
from geneweb.web.utils import BASE_DIR

templates = Jinja2Templates(directory=str(BASE_DIR / "server/templates"))
router = APIRouter()

@router.get("/base/{base_name}", response_class=HTMLResponse)
async def base_detail(request: Request, base_name: str):
    context = {
        "request": request,
        "base_name": base_name,
        # tu peux ajouter d’autres infos de la BDD ici
    }
    return templates.TemplateResponse("base_details.html", context)

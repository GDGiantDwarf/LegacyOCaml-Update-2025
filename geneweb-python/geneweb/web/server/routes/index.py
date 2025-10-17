from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from starlette.templating import Jinja2Templates
from geneweb.web.utils import BASE_DIR
from geneweb.core.database import Database

templates = Jinja2Templates(directory=str(BASE_DIR / "server/templates"))
router = APIRouter()

@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(
        request,
        "index.html",
        {"request": request, "title": "GeneWeb - Accueil"}
    )

@router.post("/select-base")
async def select_base(request: Request, base_name: str = Form(...)):
    # Ici tu peux vérifier si la base existe, etc.
    if not Database.is_base_exist(base_name):
        return templates.TemplateResponse(request, "index.html", {
            "request": request,
            "error_message": f"La base '{base_name}' n'existe pas"
        })
    url = f"/base/{base_name}"  # URL vers la page de gestion
    return RedirectResponse(url=url, status_code=303)  # PRG pattern






from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from starlette.templating import Jinja2Templates
from geneweb.web.utils import BASE_DIR
from geneweb.core.database import Database

# templates = Jinja2Templates(directory=str(BASE_DIR / "server/templates"))
router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    bases = Database.get_existing_bases()
    templates = request.app.state.templates
    context = templates.get_context(request)
    context.update({"request": request, "list_bases": bases})
    return templates.TemplateResponse(request, "index.html", context)


@router.post("/select-base/{base_name}")
async def select_base(request: Request, base_name: str):
    if not Database.is_base_exist(base_name):
        bases = Database.get_existing_bases()
        templates = request.app.state.templates
        context = templates.get_context(request)
        context.update(
            {
                "request": request,
                "list_bases": bases,
                "error_message": f"La base '{base_name}' n'existe pas",
            }
        )
        return templates.TemplateResponse(request, "index.html", context)

    return RedirectResponse(url=f"/base/{base_name}", status_code=303)

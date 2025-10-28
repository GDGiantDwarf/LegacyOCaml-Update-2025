from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from starlette.templating import Jinja2Templates
from geneweb.core.database import Database
from geneweb.web.utils import BASE_DIR

router = APIRouter()

@router.get('/create_base_empty', response_class=HTMLResponse)
async def index(request: Request):
    templates = request.app.state.templates
    context = templates.get_context(request)
    context.update({
        "request": request,
    })
    return templates.TemplateResponse(request, "create_base_empty.html", context)

@router.post("/create_base")
async def create_base(request: Request, base_name: str = Form(...), reorg: bool = Form(False)):
    try:
        database = Database(base_name=base_name)
        return {"message": f"Base '{base_name}' créée avec succès"}
    except Exception as e:
        print("An exception occurred:", e)
        return {"error": str(e)}
    
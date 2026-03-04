from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from geneweb.core.database import BaseManager

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def admin_index(request: Request):
    """
    Page principale du panneau d'administration.
    Recupere la liste des bases via BaseManager.
    """
    templates = request.app.state.templates
    bases = BaseManager.list_bases()

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "bases": bases,
        },
    )

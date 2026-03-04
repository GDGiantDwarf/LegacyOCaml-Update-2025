from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from geneweb.core.database import BaseManager

router = APIRouter(tags=["admin:pages"])


@router.get("/welcome", response_class=HTMLResponse)
async def welcome_page(request: Request):
    """Management hub with links to all operations."""
    templates = request.app.state.templates
    bases = BaseManager.list_bases()
    return templates.TemplateResponse(
        "welcome.html",
        {"request": request, "bases": bases},
    )


@router.get("/cleanup", response_class=HTMLResponse)
async def cleanup_page(request: Request):
    """Database cleanup page."""
    templates = request.app.state.templates
    bases = BaseManager.list_bases()
    return templates.TemplateResponse(
        "cleanup.html",
        {"request": request, "bases": bases},
    )


@router.get("/rename", response_class=HTMLResponse)
async def rename_page(request: Request):
    """Database rename page."""
    templates = request.app.state.templates
    bases = BaseManager.list_bases()
    return templates.TemplateResponse(
        "rename.html",
        {"request": request, "bases": bases},
    )


@router.get("/delete", response_class=HTMLResponse)
async def delete_page(request: Request):
    """Database deletion page."""
    templates = request.app.state.templates
    bases = BaseManager.list_bases()
    return templates.TemplateResponse(
        "delete.html",
        {"request": request, "bases": bases},
    )


@router.get("/merge-page", response_class=HTMLResponse)
async def merge_page(request: Request):
    """Database merge page."""
    templates = request.app.state.templates
    bases = BaseManager.list_bases()
    return templates.TemplateResponse(
        "merge.html",
        {"request": request, "bases": bases},
    )


@router.get("/list", response_class=HTMLResponse)
async def list_page(request: Request):
    """Database list page."""
    templates = request.app.state.templates
    bases = BaseManager.list_bases()
    return templates.TemplateResponse(
        "list.html",
        {"request": request, "bases": bases},
    )


@router.get("/import-page", response_class=HTMLResponse)
async def import_page(request: Request):
    """Database import page."""
    templates = request.app.state.templates
    return templates.TemplateResponse(
        "import.html",
        {"request": request},
    )


@router.get("/export-page", response_class=HTMLResponse)
async def export_page(request: Request):
    """Database export page."""
    templates = request.app.state.templates
    bases = BaseManager.list_bases()
    return templates.TemplateResponse(
        "export.html",
        {"request": request, "bases": bases},
    )


@router.get(
    "/backup-page", response_class=HTMLResponse
)
async def backup_page(request: Request):
    """Backup and restore page."""
    templates = request.app.state.templates
    bases = BaseManager.list_bases()
    return templates.TemplateResponse(
        "backup.html",
        {"request": request, "bases": bases},
    )

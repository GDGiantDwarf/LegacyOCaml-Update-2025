from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import httpx
from pathlib import Path

router = APIRouter()

templates = Jinja2Templates(directory=str(Path(__file__).resolve().parent.parent / "templates"))

@router.get("/", response_class=HTMLResponse)
async def admin_index(request: Request):
    """
    Page principale du panneau d'administration.
    Récupère dynamiquement la liste des bases via /api/bases.
    """
    bases = []
    try:
        async with httpx.AsyncClient() as client:
            r = await client.get("http://localhost:2316/api/bases")
            if r.status_code == 200:
                bases = r.json().get("bases", [])
    except Exception as e:
        print(f"[WARN] Impossible de charger les bases : {e}")

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "bases": bases,
        },
    )

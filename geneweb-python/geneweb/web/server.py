from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
import pathlib
from datetime import datetime
from ..core.database import Database
from ..core.repositories.person_repository import PersonRepository

app = FastAPI(title="Mini GeneWeb (demo)")

# Templates : le dossier 'templates' (relatif au fichier main.py)
BASE_DIR = pathlib.Path(__file__).parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates/server"))

# Optionnel : servir un répertoire static (css/js/images) si tu en ajoutes
static_dir = BASE_DIR / "static"
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("add_person.html", {"request": request})

@app.post("/addperson", response_class=HTMLResponse)
async def add_person(
        request: Request,
        base_name: str = Form(...),
        first_name: str = Form(...),
        last_name: str = Form(...),
        gender: str = Form(None),
        birth_date: str = Form(None),
        death_date: str = Form(None),
        birth_place: str = Form(None),
        death_place: str = Form(None),
        occupation: str = Form(None),
        notes: str = Form(None),
    ):
    db = Database(base_name)
    repo = PersonRepository(db.session)

    repo.add_person(
        first_name=first_name,
        last_name=last_name,
        gender=gender,
        birth_date=datetime.strptime(birth_date, "%Y-%m-%d").date(),
        death_date=death_date,
        birth_place=birth_place,
        death_place=death_place,
        occupation=occupation,
        notes=notes
    )
    db.close()
    return RedirectResponse(url=f"/persons/{base_name}", status_code=303)


# --- Page listant toutes les personnes d’une base ---
@app.get("/persons/{base_name}", response_class=HTMLResponse)
async def list_persons(request: Request, base_name: str):
    #db = Database(base_name)
    #persons = db.get_all_persons()
    #db.close()
    return templates.TemplateResponse(
        "persons.html",
        {"request": request, "base_name": base_name}
    )
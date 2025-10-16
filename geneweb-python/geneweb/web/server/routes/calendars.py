from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from starlette.templating import Jinja2Templates
from geneweb.web.utils import BASE_DIR
from geneweb.core.database import Database

templates = Jinja2Templates(directory=str(BASE_DIR / "server/templates"))
router = APIRouter()

from geneweb.core.repositories.calendar_repository import CalendarRepository
from geneweb.core.services.calendar_converter import CalendarConverter

@router.get("/calendars", response_class=HTMLResponse)
async def calendars_converter(request: Request):
    return templates.TemplateResponse(
        "calendars.html",
        {"request": request}
    )


@router.post("/api/convert-date")
async def convert_date(
    year: int = Form(...),
    month: int = Form(...),
    day: int = Form(...)
):
    """API endpoint pour convertir une date"""
    converter = CalendarConverter()
    result = converter.convert_from_gregorian(year, month, day)
    return result


@router.post("/api/save-calendar-date")
async def save_calendar_date(
    base_name: str = Form(...),
    person_id: int = Form(None),
    event_type: str = Form(...),
    year: int = Form(...),
    month: int = Form(...),
    day: int = Form(...)
):
    """Enregistre une date convertie dans la base"""
    db = Database(base_name)
    repo = CalendarRepository(db.session)
    
    calendar_date = repo.add_calendar_date(
        person_id=person_id,
        event_type=event_type,
        gregorian_year=year,
        gregorian_month=month,
        gregorian_day=day
    )
    
    db.close()
    return {
        "success": True,
        "id": calendar_date.id,
        "julian_day_number": calendar_date.julian_day_number
    }
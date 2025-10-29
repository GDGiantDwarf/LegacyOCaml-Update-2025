from sqlalchemy.orm import Session
from datetime import date
from typing import Optional, List
from ..models.Calendar_date import CalendarDate
from ..services.calendar_converter import CalendarConverter


class CalendarRepository:
    def __init__(self, session: Session):
        self.session = session
        self.converter = CalendarConverter()

    def add_calendar_date(
        self,
        person_id: Optional[int],
        event_type: str,
        gregorian_year: int,
        gregorian_month: int,
        gregorian_day: int,
    ) -> CalendarDate:

        # Conversion vers tous les calendriers
        conversions = self.converter.convert_from_gregorian(
            gregorian_year, gregorian_month, gregorian_day
        )

        julian = conversions["julian"]
        french = conversions["french_republican"]
        hebrew = conversions["hebrew"]

        calendar_date = CalendarDate(
            person_id=person_id,
            event_type=event_type,
            gregorian_year=gregorian_year,
            gregorian_month=gregorian_month,
            gregorian_day=gregorian_day,
            gregorian_date=date(
                gregorian_year,
                gregorian_month,
                gregorian_day),
            julian_year=julian["year"],
            julian_month=julian["month"],
            julian_day=julian["day"],
            julian_day_number=conversions["julian_day_number"],
            french_year=french["year"] if french else None,
            french_month=french["month_name"] if french else None,
            french_day=french["day"] if french else None,
            hebrew_year=hebrew["year"],
            hebrew_month=hebrew["month_name"],
            hebrew_day=hebrew["day"],
        )

        self.session.add(calendar_date)
        self.session.commit()
        self.session.refresh(calendar_date)

        return calendar_date

    def get_calendar_dates_by_person(
            self, person_id: int) -> List[CalendarDate]:
        return (
            self.session.query(CalendarDate)
            .filter(CalendarDate.person_id == person_id)
            .all()
        )

    def get_calendar_date_by_id(self, date_id: int) -> Optional[CalendarDate]:
        return (
            self.session.query(CalendarDate).filter(
                CalendarDate.id == date_id).first())

    def delete_calendar_date(self, date_id: int) -> bool:
        calendar_date = self.get_calendar_date_by_id(date_id)
        if calendar_date:
            self.session.delete(calendar_date)
            self.session.commit()
            return True
        return False

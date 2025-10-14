from sqlalchemy.orm import Session
from datetime import date
from geneweb.core.models.Event import Event

class EventRepository:
    def __init__(self, session: Session):
        self.session = session

    def add_event(self, event_type: str, date: date = None, place: str = None, description: str = None,
                person_id: int = None, family_id: int = None, source_id: int = None):
        event = Event(
            event_type=event_type,
            date=date,
            place=place,
            description=description,
            person_id=person_id,
            family_id=family_id,
            source_id=source_id
        )
        self.session.add(event)
        self.session.commit()
        return event
    
    def get_event_by_id(self, event_id):
        return self.session.query(Event).filter(Event.id == event_id).first()
    
    def update_event_by_id(self, event_id: int, event_type: str = None, date: date = None, place: str = None, description: str = None,
                        person_id: int = None, family_id: int = None, source_id: int = None):
        event = self.get_event_by_id(event_id)
        new_event = Event(
            event_type=event_type,
            date=date,
            place=place,
            description=description,
            person_id=person_id,
            family_id=family_id,
            source_id=source_id
        )
        if not event:
            raise ValueError("event_id is invalid")
    
        for attr, value in vars(new_event).items():
            if attr != "id" and value is not None:
                setattr(event, attr, value)
        self.session.commit()
        return event
    
    def delete_event_by_id(self, event_id):
        event = self.get_event_by_id(event_id)
        if event:
            self.session.delete(event)
            self.session.commit()
            return True
        return False
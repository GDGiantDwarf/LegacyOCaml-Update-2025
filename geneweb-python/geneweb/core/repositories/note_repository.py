from sqlalchemy.orm import Session
from geneweb.core.models.Note import Note

class NoteRepository:
    def __init__(self, session: Session):
        self.session = session

    def add_note(self, content: str, person_id: int = None, event_id: int = None):
        note = Note(
            content=content,
            person_id=person_id,
            event_id=event_id
        )
        self.session.add(note)
        self.session.commit()
        return note
    
    def get_note_by_id(self, note_id):
        return self.session.query(Note).filter(Note.id == note_id).first()
    
    def update_note_by_id(self, note_id, content: str = None, person_id: int = None, event_id: int = None):
        note = self.get_note_by_id(note_id)
        new_note = Note(
            content=content,
            person_id=person_id,
            event_id=event_id
        )
        if not note:
            raise ValueError("note_id is invalid")
    
        for attr, value in vars(new_note).items():
            if attr != "id" and value is not None:
                setattr(note, attr, value)
        self.session.commit()
        return note
    
    def delete_note_by_id(self, note_id):
        note = self.get_note_by_id(note_id)
        if note:
            self.session.delete(note)
            self.session.commit()
            return True
        return False
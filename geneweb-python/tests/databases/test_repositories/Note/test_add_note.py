from conftest import db
from geneweb.core.repositories.note_repository import NoteRepository

def test_add_note(db):
    repo = NoteRepository(db.session)

    note = repo.add_note("content")
    assert note is not None
    assert note.content == "content"
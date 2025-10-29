from conftest import db
from geneweb.core.repositories.note_repository import NoteRepository


def test_add_and_delete_an_note(db):
    repo = NoteRepository(db.session)

    note = repo.add_note("content")
    assert note is not None
    assert note.content == "content"

    deleted_note = repo.delete_note_by_id(note.id)
    assert deleted_note


def test_add_and_delete_a_wrong_event(db):
    repo = NoteRepository(db.session)

    note = repo.add_note("content")
    assert note is not None
    assert note.content == "content"

    deleted_note = repo.delete_note_by_id(4)
    assert deleted_note is False

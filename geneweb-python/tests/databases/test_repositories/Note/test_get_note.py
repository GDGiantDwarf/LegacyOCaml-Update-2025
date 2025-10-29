from conftest import db
from geneweb.core.repositories.note_repository import NoteRepository


def test_add_one_note_and_get_it(db):
    repo = NoteRepository(db.session)
    content = "content"

    note = repo.add_note(content)
    assert note is not None
    assert note.content == content

    get_note = repo.get_note_by_id(note.id)
    assert get_note is not None
    assert get_note.content == content


def test_add_one_note_and_get_a_wrong_one(db):
    repo = NoteRepository(db.session)
    content = "content"

    note = repo.add_note(content)
    assert note is not None
    assert note.content == content

    get_note = repo.get_note_by_id(4)
    assert get_note is None

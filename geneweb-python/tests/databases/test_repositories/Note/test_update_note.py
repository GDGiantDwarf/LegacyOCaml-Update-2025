import pytest
from conftest import db
from geneweb.core.repositories.note_repository import NoteRepository

def test_update_note(db):
    repo = NoteRepository(db.session)
    content = "content"
    updated_content = "new content"

    note = repo.add_note(content)
    assert note is not None
    assert note.content == content

    repo.update_note_by_id(note.id, content=updated_content)

    get_note = repo.get_note_by_id(note.id)
    assert get_note is not None
    assert get_note.content == updated_content

def test_update_note_with_wrong_note_id(db):
    repo = NoteRepository(db.session)
    content = "content"
    updated_content = "new content"

    note = repo.add_note(content)
    assert note is not None
    assert note.content == content

    with pytest.raises(ValueError) as excinfo:
        repo.update_note_by_id(3, content=updated_content)

    assert "note_id is invalid" in str(excinfo.value)
import pytest
from conftest import db
from geneweb.core.repositories.media_repository import MediaRepository

def test_update_media(db):
    repo = MediaRepository(db.session)
    file_path = "path"
    updated_file_path = "new/path"

    note = repo.add_media(file_path=file_path)
    assert note is not None
    assert note.file_path == file_path

    repo.update_media_by_id(note.id, file_path=updated_file_path)

    get_note = repo.get_media_by_id(note.id)
    assert get_note is not None
    assert get_note.file_path == updated_file_path

def test_update_media_with_wrong_media_id(db):
    repo = MediaRepository(db.session)
    file_path = "path"
    updated_file_path = "new/path"

    note = repo.add_media(file_path=file_path)
    assert note is not None
    assert note.file_path == file_path

    with pytest.raises(ValueError) as excinfo:
        repo.update_media_by_id(4, file_path=updated_file_path)

    assert "media_id is invalid" in str(excinfo.value)
from conftest import db
from geneweb.core.repositories.media_repository import MediaRepository

def test_add_one_media_and_get_it(db):
    repo = MediaRepository(db.session)
    file_path = "path"

    note = repo.add_media(file_path=file_path)
    assert note is not None
    assert note.file_path == file_path

    get_note = repo.get_media_by_id(note.id)
    assert get_note is not None
    assert get_note.file_path == file_path

def test_add_one_media_and_get_a_wrong_one(db):
    repo = MediaRepository(db.session)
    file_path = "path"

    note = repo.add_media(file_path=file_path)
    assert note is not None
    assert note.file_path == file_path

    get_note = repo.get_media_by_id(4)
    assert get_note is None
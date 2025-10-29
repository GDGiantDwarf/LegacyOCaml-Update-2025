from conftest import db
from geneweb.core.repositories.media_repository import MediaRepository


def test_add_media(db):
    repo = MediaRepository(db.session)
    file_path = "path"

    note = repo.add_media(file_path=file_path)
    assert note is not None
    assert note.file_path == file_path

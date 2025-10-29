from conftest import db
from geneweb.core.repositories.media_repository import MediaRepository


def test_delete_media(db):
    repo = MediaRepository(db.session)
    file_path = "path"

    media = repo.add_media(file_path=file_path)
    assert media is not None
    assert media.file_path == file_path

    deleted_media = repo.delete_media_by_id(media.id)
    assert deleted_media


def test_delete_media_with_wrong_id(db):
    repo = MediaRepository(db.session)
    file_path = "path"

    media = repo.add_media(file_path=file_path)
    assert media is not None
    assert media.file_path == file_path

    deleted_media = repo.delete_media_by_id(4)
    assert deleted_media is False

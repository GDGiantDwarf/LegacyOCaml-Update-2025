from conftest import db
from datetime import date
from geneweb.core.repositories.source_repository import SourceRepository

def test_add_one_source(db):
    repo = SourceRepository(db.session)

    title = "title"
    reference = "reference"
    type = "mp4"

    source = repo.add_source(title, reference, type)
    assert source is not None
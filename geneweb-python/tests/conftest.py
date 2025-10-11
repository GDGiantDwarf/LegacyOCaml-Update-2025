import pytest
from geneweb.core.database import Database

@pytest.fixture
def db():
    db = Database(in_memory=True)
    yield db
    db.close()
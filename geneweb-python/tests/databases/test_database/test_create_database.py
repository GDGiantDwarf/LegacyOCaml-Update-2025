import pytest
from pathlib import Path
from geneweb.core.database import Database
import shutil

def test_create_file_database(tmp_path):

    bases_folder = tmp_path / "test_databases"
    db_name = "test_db"

    Database.BASES_FOLDER = bases_folder

    db = Database(db_name)

    assert bases_folder.exists() and bases_folder.is_dir()

    db_path = bases_folder / f"{db_name}.db"
    assert db_path.exists() and db_path.is_file()

    db.close()

    shutil.rmtree(tmp_path)

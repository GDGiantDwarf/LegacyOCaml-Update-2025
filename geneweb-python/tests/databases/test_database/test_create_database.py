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


def test_database_already_exits(tmp_path):
    Database.BASES_FOLDER = tmp_path

    db_name = "test_db"
    db_path = tmp_path / f"{db_name}.db"

    db_path.touch()

    with pytest.raises(FileExistsError) as excinfo:
        Database(base_name=db_name)

    assert "already exists" in str(excinfo.value)

    shutil.rmtree(tmp_path)


def test_create_database_with_none_name(tmp_path):
    Database.BASES_FOLDER = tmp_path

    with pytest.raises(ValueError) as excinfo:
        Database(base_name=None)

    assert "base_name must be provided" in str(excinfo.value)

    shutil.rmtree(tmp_path)

def test_create_database_with_empty_name(tmp_path):
    Database.BASES_FOLDER = tmp_path

    with pytest.raises(ValueError) as excinfo:
        Database(base_name="")

    assert "base_name must be provided" in str(excinfo.value)

    shutil.rmtree(tmp_path)
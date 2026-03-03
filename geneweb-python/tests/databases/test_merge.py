import sqlite3
from pathlib import Path

import pytest

from geneweb.core.database import BaseManager

# ------------------------------------------------------
# FIXTURES
# ------------------------------------------------------


@pytest.fixture
def base_dir(tmp_path) -> Path:
    """Create a temporary directory for test bases."""
    d = tmp_path / "bases"
    d.mkdir()
    return d


def _create_base_with_table(
    base_dir: Path,
    name: str,
    rows: list[tuple[int, str]],
):
    """Helper: create a base with a 'people' table."""
    BaseManager.create_base(name, base_dir)
    path = BaseManager.base_path(name, base_dir)
    con = sqlite3.connect(str(path))
    con.execute(
        "CREATE TABLE people "
        "(id INTEGER PRIMARY KEY, name TEXT)"
    )
    con.executemany(
        "INSERT INTO people VALUES (?, ?)", rows
    )
    con.commit()
    con.close()


# ------------------------------------------------------
# TESTS
# ------------------------------------------------------


def test_merge_two_bases(base_dir):
    """Merge two bases and verify the target has both."""
    _create_base_with_table(
        base_dir, "alpha", [(1, "Alice")]
    )
    _create_base_with_table(
        base_dir, "bravo", [(2, "Bob")]
    )

    BaseManager.merge_bases(
        "alpha", "bravo", "merged", base_dir
    )

    target = BaseManager.base_path("merged", base_dir)
    assert target.exists()

    con = sqlite3.connect(str(target))
    rows = con.execute(
        "SELECT id, name FROM people ORDER BY id"
    ).fetchall()
    con.close()

    assert len(rows) == 2
    assert rows[0] == (1, "Alice")
    assert rows[1] == (2, "Bob")


def test_merge_nonexistent_source(base_dir):
    """Merging with a missing source raises error."""
    _create_base_with_table(
        base_dir, "exists", [(1, "X")]
    )

    with pytest.raises(FileNotFoundError):
        BaseManager.merge_bases(
            "exists", "ghost", "out", base_dir
        )

    with pytest.raises(FileNotFoundError):
        BaseManager.merge_bases(
            "ghost", "exists", "out", base_dir
        )


def test_merge_existing_target(base_dir):
    """Merging into an existing target raises error."""
    _create_base_with_table(
        base_dir, "one", [(1, "A")]
    )
    _create_base_with_table(
        base_dir, "two", [(2, "B")]
    )
    _create_base_with_table(
        base_dir, "taken", [(3, "C")]
    )

    with pytest.raises(FileExistsError):
        BaseManager.merge_bases(
            "one", "two", "taken", base_dir
        )


def test_merge_invalid_name(base_dir):
    """An invalid target name raises ValueError."""
    _create_base_with_table(
        base_dir, "ok1", [(1, "A")]
    )
    _create_base_with_table(
        base_dir, "ok2", [(2, "B")]
    )

    with pytest.raises(ValueError):
        BaseManager.merge_bases(
            "ok1", "ok2", "bad name!", base_dir
        )

from datetime import date

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from geneweb.core.services.gedcom_converter import (
    _format_date,
    _parse_date,
    _parse_name,
    export_to_gedcom,
    import_from_gedcom,
)
from geneweb.core.models.alchemyBase import Base
from geneweb.core.models.Person import Person
from geneweb.core.models.Family import Family
from geneweb.core.models.ChildInFamily import ChildInFamily


def _make_session():
    """Create an in-memory SQLAlchemy session."""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
    )
    Base.metadata.create_all(bind=engine)
    session_factory = sessionmaker(bind=engine)
    return session_factory()


# ---------------------------------------------------
# _format_date
# ---------------------------------------------------


def test_format_date():
    result = _format_date(date(1990, 1, 15))
    assert result == "15 JAN 1990"


def test_format_date_none():
    assert _format_date(None) is None


# ---------------------------------------------------
# _parse_date
# ---------------------------------------------------


def test_parse_date_full():
    result = _parse_date("15 JAN 1990")
    assert result == date(1990, 1, 15)


def test_parse_date_month_year():
    result = _parse_date("MAR 2000")
    assert result == date(2000, 3, 1)


def test_parse_date_year():
    result = _parse_date("1850")
    assert result == date(1850, 1, 1)


def test_parse_date_empty():
    assert _parse_date("") is None


def test_parse_date_invalid():
    assert _parse_date("garbage") is None


# ---------------------------------------------------
# _parse_name
# ---------------------------------------------------


def test_parse_name_full():
    record = {
        "first_name": "",
        "last_name": "",
    }
    _parse_name(record, "John /Doe/")
    assert record["first_name"] == "John"
    assert record["last_name"] == "Doe"


def test_parse_name_no_surname():
    record = {
        "first_name": "",
        "last_name": "",
    }
    _parse_name(record, "John")
    assert record["first_name"] == "John"


# ---------------------------------------------------
# export_to_gedcom
# ---------------------------------------------------


def test_export_empty_db():
    session = _make_session()
    content = export_to_gedcom(session)
    assert "0 HEAD" in content
    assert "0 TRLR" in content
    session.close()


def test_export_with_data():
    session = _make_session()
    p1 = Person(
        first_name="John",
        last_name="Doe",
        gender="M",
        birth_date=date(1980, 5, 20),
    )
    p2 = Person(
        first_name="Jane",
        last_name="Doe",
        gender="F",
    )
    session.add_all([p1, p2])
    session.flush()
    fam = Family(
        spouse1_id=p1.id,
        spouse2_id=p2.id,
        marriage_date=date(2005, 6, 15),
    )
    session.add(fam)
    session.flush()
    cif = ChildInFamily(
        person_id=p1.id,
        family_id=fam.id,
    )
    session.add(cif)
    session.commit()

    content = export_to_gedcom(session)
    assert "John /Doe/" in content
    assert "Jane /Doe/" in content
    assert "@F" in content
    assert "HUSB" in content
    assert "WIFE" in content
    assert "15 JUN 2005" in content
    session.close()


# ---------------------------------------------------
# import_from_gedcom
# ---------------------------------------------------


def test_import_basic():
    session = _make_session()
    gedcom = (
        "0 HEAD\n"
        "1 SOUR TEST\n"
        "0 @I1@ INDI\n"
        "1 NAME John /Doe/\n"
        "1 SEX M\n"
        "1 BIRT\n"
        "2 DATE 15 JAN 1990\n"
        "0 @I2@ INDI\n"
        "1 NAME Jane /Smith/\n"
        "1 SEX F\n"
        "0 @F1@ FAM\n"
        "1 HUSB @I1@\n"
        "1 WIFE @I2@\n"
        "1 MARR\n"
        "2 DATE 10 JUN 2015\n"
        "1 CHIL @I1@\n"
        "0 TRLR\n"
    )
    result = import_from_gedcom(gedcom, session)
    assert result["persons"] == 2
    assert result["families"] == 1

    persons = session.query(Person).all()
    assert len(persons) == 2
    session.close()


def test_roundtrip():
    session = _make_session()
    p = Person(
        first_name="Alice",
        last_name="Wonder",
        gender="F",
        birth_date=date(1995, 3, 10),
        occupation="Engineer",
    )
    session.add(p)
    session.commit()

    exported = export_to_gedcom(session)
    session.close()

    session2 = _make_session()
    result = import_from_gedcom(exported, session2)
    assert result["persons"] == 1

    imported = session2.query(Person).first()
    assert imported.first_name == "Alice"
    assert imported.last_name == "Wonder"
    assert imported.gender == "F"
    assert imported.birth_date == date(1995, 3, 10)
    assert imported.occupation == "Engineer"
    session2.close()


def test_import_empty():
    session = _make_session()
    result = import_from_gedcom(
        "0 HEAD\n0 TRLR\n", session
    )
    assert result["persons"] == 0
    assert result["families"] == 0
    session.close()


def test_export_with_death_and_notes():
    """Export person with death, notes, occupation."""
    session = _make_session()
    p = Person(
        first_name="Old",
        last_name="Timer",
        gender="M",
        birth_date=date(1900, 1, 1),
        birth_place="London",
        death_date=date(1980, 12, 31),
        death_place="Oxford",
        occupation="Professor",
        notes="A notable person",
    )
    session.add(p)
    session.commit()
    content = export_to_gedcom(session)
    assert "Old /Timer/" in content
    assert "1 BIRT" in content
    assert "2 PLAC London" in content
    assert "1 DEAT" in content
    assert "2 PLAC Oxford" in content
    assert "1 OCCU Professor" in content
    assert "1 NOTE A notable person" in content
    session.close()


def test_export_family_with_divorce():
    """Export family with divorce and notes."""
    session = _make_session()
    p1 = Person(
        first_name="A", last_name="B", gender="M"
    )
    p2 = Person(
        first_name="C", last_name="D", gender="F"
    )
    session.add_all([p1, p2])
    session.flush()
    fam = Family(
        spouse1_id=p1.id,
        spouse2_id=p2.id,
        marriage_date=date(2000, 1, 1),
        marriage_place="Rome",
        divorce_date=date(2010, 6, 15),
        notes="Divorced",
    )
    session.add(fam)
    session.commit()
    content = export_to_gedcom(session)
    assert "1 MARR" in content
    assert "2 PLAC Rome" in content
    assert "1 DIV" in content
    assert "15 JUN 2010" in content
    assert "1 NOTE Divorced" in content
    session.close()


def test_import_with_birth_place():
    """Import GEDCOM with birth place."""
    session = _make_session()
    gedcom = (
        "0 HEAD\n"
        "0 @I1@ INDI\n"
        "1 NAME Bob /Builder/\n"
        "1 SEX M\n"
        "1 BIRT\n"
        "2 DATE 5 MAR 1975\n"
        "2 PLAC Manchester\n"
        "1 DEAT\n"
        "2 DATE 20 OCT 2020\n"
        "2 PLAC London\n"
        "1 OCCU Builder\n"
        "1 NOTE A builder\n"
        "0 TRLR\n"
    )
    result = import_from_gedcom(gedcom, session)
    assert result["persons"] == 1
    p = session.query(Person).first()
    assert p.first_name == "Bob"
    assert p.last_name == "Builder"
    assert p.birth_place == "Manchester"
    assert p.death_place == "London"
    assert p.occupation == "Builder"
    assert p.notes == "A builder"
    session.close()


def test_import_family_with_divorce():
    """Import GEDCOM family with divorce."""
    session = _make_session()
    gedcom = (
        "0 HEAD\n"
        "0 @I1@ INDI\n"
        "1 NAME X /Y/\n"
        "1 SEX M\n"
        "0 @I2@ INDI\n"
        "1 NAME A /B/\n"
        "1 SEX F\n"
        "0 @F1@ FAM\n"
        "1 HUSB @I1@\n"
        "1 WIFE @I2@\n"
        "1 MARR\n"
        "2 DATE 1 JAN 2000\n"
        "2 PLAC Paris\n"
        "1 DIV\n"
        "2 DATE 1 JAN 2010\n"
        "1 NOTE Family note\n"
        "0 TRLR\n"
    )
    result = import_from_gedcom(gedcom, session)
    assert result["persons"] == 2
    assert result["families"] == 1
    fam = session.query(Family).first()
    assert fam.marriage_place == "Paris"
    assert fam.divorce_date == date(2010, 1, 1)
    assert fam.notes == "Family note"
    session.close()


def test_import_givn_surn_subtags():
    """Import GEDCOM with GIVN and SURN sub-tags."""
    session = _make_session()
    gedcom = (
        "0 HEAD\n"
        "0 @I1@ INDI\n"
        "1 NAME Ignored /Ignored/\n"
        "2 GIVN RealFirst\n"
        "2 SURN RealLast\n"
        "0 TRLR\n"
    )
    result = import_from_gedcom(gedcom, session)
    assert result["persons"] == 1
    p = session.query(Person).first()
    assert p.first_name == "RealFirst"
    assert p.last_name == "RealLast"
    session.close()


def test_extract_xref_id():
    """Test _extract_xref_id helper."""
    from geneweb.core.services.gedcom_converter \
        import _extract_xref_id
    assert _extract_xref_id("@I42@") == 42
    assert _extract_xref_id("@F1@") == 1
    assert _extract_xref_id("@X1@") is None
    assert _extract_xref_id("") is None
    assert _extract_xref_id("@Iabc@") is None

"""GEDCOM 5.5.1 import/export converter service."""

from datetime import date, datetime
from typing import Dict, List, Optional

from sqlalchemy.orm import Session

from geneweb.core.models.Person import Person
from geneweb.core.models.Family import Family
from geneweb.core.models.ChildInFamily import ChildInFamily


GEDCOM_MONTHS: List[str] = [
    "JAN", "FEB", "MAR", "APR", "MAY", "JUN",
    "JUL", "AUG", "SEP", "OCT", "NOV", "DEC",
]


def _format_date(d: Optional[date]) -> Optional[str]:
    """Convert a Python date to GEDCOM date string.

    Format: DD MMM YYYY (e.g. 15 JAN 1990).
    """
    if d is None:
        return None
    month_str = GEDCOM_MONTHS[d.month - 1]
    return f"{d.day} {month_str} {d.year}"


def _parse_date(text: str) -> Optional[date]:
    """Parse a GEDCOM date string into a Python date.

    Supports formats:
    - DD MMM YYYY
    - MMM YYYY
    - YYYY
    """
    text = text.strip()
    if not text:
        return None
    parts = text.split()
    try:
        if len(parts) == 3:
            day = int(parts[0])
            month = GEDCOM_MONTHS.index(parts[1].upper()) + 1
            year = int(parts[2])
            return date(year, month, day)
        if len(parts) == 2:
            month = GEDCOM_MONTHS.index(parts[0].upper()) + 1
            year = int(parts[1])
            return date(year, month, 1)
        if len(parts) == 1:
            year = int(parts[0])
            return date(year, 1, 1)
    except (ValueError, IndexError):
        return None
    return None


def _build_header() -> str:
    """Build the GEDCOM file header."""
    now = datetime.now()
    date_str = f"{now.day} {GEDCOM_MONTHS[now.month - 1]} {now.year}"
    lines: List[str] = [
        "0 HEAD",
        "1 SOUR GeneWeb-Python",
        "2 VERS 1.0",
        "2 NAME GeneWeb-Python",
        "1 DEST ANY",
        f"1 DATE {date_str}",
        "1 GEDC",
        "2 VERS 5.5.1",
        "2 FORM LINEAGE-LINKED",
        "1 CHAR UTF-8",
    ]
    return "\n".join(lines)


def _person_to_indi(person: Person) -> str:
    """Convert a Person model to a GEDCOM INDI record."""
    lines: List[str] = [
        f"0 @I{person.id}@ INDI",
    ]

    first = person.first_name or ""
    last = person.last_name or ""
    lines.append(f"1 NAME {first} /{last}/")
    if first:
        lines.append(f"2 GIVN {first}")
    if last:
        lines.append(f"2 SURN {last}")

    if person.gender:
        sex = person.gender.upper()
        if sex in ("M", "F"):
            lines.append(f"1 SEX {sex}")

    if person.birth_date or person.birth_place:
        lines.append("1 BIRT")
        if person.birth_date:
            lines.append(
                f"2 DATE {_format_date(person.birth_date)}"
            )
        if person.birth_place:
            lines.append(f"2 PLAC {person.birth_place}")

    if person.death_date or person.death_place:
        lines.append("1 DEAT")
        if person.death_date:
            lines.append(
                f"2 DATE {_format_date(person.death_date)}"
            )
        if person.death_place:
            lines.append(f"2 PLAC {person.death_place}")

    if person.occupation:
        lines.append(f"1 OCCU {person.occupation}")

    if person.notes:
        lines.append(f"1 NOTE {person.notes}")

    return "\n".join(lines)


def _family_to_fam(
    family: Family,
    children_ids: List[int],
) -> str:
    """Convert a Family model to a GEDCOM FAM record."""
    lines: List[str] = [
        f"0 @F{family.id}@ FAM",
    ]

    if family.spouse1_id:
        lines.append(f"1 HUSB @I{family.spouse1_id}@")
    if family.spouse2_id:
        lines.append(f"1 WIFE @I{family.spouse2_id}@")

    if family.marriage_date or family.marriage_place:
        lines.append("1 MARR")
        if family.marriage_date:
            lines.append(
                f"2 DATE {_format_date(family.marriage_date)}"
            )
        if family.marriage_place:
            lines.append(
                f"2 PLAC {family.marriage_place}"
            )

    if family.divorce_date:
        lines.append("1 DIV")
        lines.append(
            f"2 DATE {_format_date(family.divorce_date)}"
        )

    for child_id in children_ids:
        lines.append(f"1 CHIL @I{child_id}@")

    if family.notes:
        lines.append(f"1 NOTE {family.notes}")

    return "\n".join(lines)


def export_to_gedcom(session: Session) -> str:
    """Export all persons and families to GEDCOM 5.5.1.

    Args:
        session: SQLAlchemy session connected to the base.

    Returns:
        Complete GEDCOM file content as a string.
    """
    parts: List[str] = [_build_header()]

    persons: List[Person] = session.query(Person).all()
    for person in persons:
        parts.append(_person_to_indi(person))

    families: List[Family] = session.query(Family).all()
    children: List[ChildInFamily] = (
        session.query(ChildInFamily).all()
    )

    family_children: Dict[int, List[int]] = {}
    for child in children:
        family_children.setdefault(
            child.family_id, []
        ).append(child.person_id)

    for family in families:
        kids = family_children.get(family.id, [])
        parts.append(_family_to_fam(family, kids))

    parts.append("0 TRLR")
    return "\n".join(parts) + "\n"


def _extract_xref_id(tag_value: str) -> Optional[int]:
    """Extract numeric ID from a GEDCOM xref like @I42@.

    Returns None if the format is invalid.
    """
    tag_value = tag_value.strip().strip("@")
    if not tag_value:
        return None
    prefix = tag_value[0]
    digits = tag_value[1:]
    if prefix in ("I", "F") and digits.isdigit():
        return int(digits)
    return None


def import_from_gedcom(
    gedcom_text: str,
    session: Session,
) -> Dict[str, int]:
    """Import GEDCOM text into the database.

    Args:
        gedcom_text: Full content of a GEDCOM file.
        session: SQLAlchemy session for the target base.

    Returns:
        Dict with counts: {"persons": N, "families": N}.
    """
    lines = gedcom_text.replace("\r\n", "\n").split("\n")

    persons_data: List[Dict] = []
    families_data: List[Dict] = []

    current_record: Optional[Dict] = None
    current_type: Optional[str] = None
    current_sub: Optional[str] = None

    for raw_line in lines:
        line = raw_line.strip()
        if not line:
            continue

        parts = line.split(None, 2)
        if len(parts) < 2:
            continue

        level = parts[0]
        if not level.isdigit():
            continue
        level_int = int(level)

        tag = parts[1]
        value = parts[2] if len(parts) > 2 else ""

        if level_int == 0:
            if current_record and current_type:
                if current_type == "INDI":
                    persons_data.append(current_record)
                elif current_type == "FAM":
                    families_data.append(current_record)
            current_record = None
            current_type = None
            current_sub = None

            if value == "INDI" or tag.endswith("INDI"):
                xref = tag if value == "INDI" else value
                current_type = "INDI"
                current_record = {
                    "xref": xref,
                    "first_name": "",
                    "last_name": "",
                    "gender": None,
                    "birth_date": None,
                    "birth_place": None,
                    "death_date": None,
                    "death_place": None,
                    "occupation": None,
                    "notes": None,
                }
            elif value == "FAM" or tag.endswith("FAM"):
                xref = tag if value == "FAM" else value
                current_type = "FAM"
                current_record = {
                    "xref": xref,
                    "spouse1_xref": None,
                    "spouse2_xref": None,
                    "marriage_date": None,
                    "marriage_place": None,
                    "divorce_date": None,
                    "children_xrefs": [],
                    "notes": None,
                }
            continue

        if current_record is None:
            continue

        if level_int == 1:
            current_sub = tag
            if current_type == "INDI":
                _parse_indi_tag(
                    current_record, tag, value
                )
            elif current_type == "FAM":
                _parse_fam_tag(
                    current_record, tag, value
                )
        elif level_int == 2:
            if current_type == "INDI":
                _parse_indi_sub(
                    current_record, current_sub,
                    tag, value,
                )
            elif current_type == "FAM":
                _parse_fam_sub(
                    current_record, current_sub,
                    tag, value,
                )

    if current_record and current_type:
        if current_type == "INDI":
            persons_data.append(current_record)
        elif current_type == "FAM":
            families_data.append(current_record)

    xref_to_person_id: Dict[str, int] = {}

    for pdata in persons_data:
        person = Person(
            first_name=pdata["first_name"] or "?",
            last_name=pdata["last_name"] or "?",
            gender=pdata["gender"],
            birth_date=pdata["birth_date"],
            birth_place=pdata["birth_place"],
            death_date=pdata["death_date"],
            death_place=pdata["death_place"],
            occupation=pdata["occupation"],
            notes=pdata["notes"],
        )
        session.add(person)
        session.flush()
        xref_to_person_id[pdata["xref"]] = person.id

    family_count = 0
    for fdata in families_data:
        sp1_xref = fdata["spouse1_xref"]
        sp2_xref = fdata["spouse2_xref"]
        sp1_id = (
            xref_to_person_id.get(sp1_xref)
            if sp1_xref else None
        )
        sp2_id = (
            xref_to_person_id.get(sp2_xref)
            if sp2_xref else None
        )

        family = Family(
            spouse1_id=sp1_id,
            spouse2_id=sp2_id,
            marriage_date=fdata["marriage_date"],
            marriage_place=fdata["marriage_place"],
            divorce_date=fdata["divorce_date"],
            notes=fdata["notes"],
        )
        session.add(family)
        session.flush()
        family_count += 1

        for child_xref in fdata["children_xrefs"]:
            child_id = xref_to_person_id.get(child_xref)
            if child_id:
                cif = ChildInFamily(
                    person_id=child_id,
                    family_id=family.id,
                )
                session.add(cif)

    session.commit()

    return {
        "persons": len(persons_data),
        "families": family_count,
    }


def _parse_indi_tag(
    record: Dict, tag: str, value: str
) -> None:
    """Parse a level-1 tag inside an INDI record."""
    if tag == "NAME":
        _parse_name(record, value)
    elif tag == "SEX":
        val = value.strip().upper()
        if val in ("M", "F"):
            record["gender"] = val
    elif tag == "OCCU":
        record["occupation"] = value.strip()
    elif tag == "NOTE":
        record["notes"] = value.strip()


def _parse_name(record: Dict, value: str) -> None:
    """Parse GEDCOM NAME value like 'John /Doe/'."""
    value = value.strip()
    if "/" in value:
        idx_start = value.index("/")
        idx_end = value.rindex("/")
        first = value[:idx_start].strip()
        last = value[idx_start + 1:idx_end].strip()
        record["first_name"] = first
        record["last_name"] = last
    else:
        record["first_name"] = value


def _parse_indi_sub(
    record: Dict,
    parent_tag: Optional[str],
    tag: str,
    value: str,
) -> None:
    """Parse a level-2 tag inside an INDI record."""
    if parent_tag == "BIRT":
        if tag == "DATE":
            record["birth_date"] = _parse_date(value)
        elif tag == "PLAC":
            record["birth_place"] = value.strip()
    elif parent_tag == "DEAT":
        if tag == "DATE":
            record["death_date"] = _parse_date(value)
        elif tag == "PLAC":
            record["death_place"] = value.strip()
    elif parent_tag == "NAME":
        if tag == "GIVN":
            record["first_name"] = value.strip()
        elif tag == "SURN":
            record["last_name"] = value.strip()


def _parse_fam_tag(
    record: Dict, tag: str, value: str
) -> None:
    """Parse a level-1 tag inside a FAM record."""
    if tag == "HUSB":
        record["spouse1_xref"] = value.strip()
    elif tag == "WIFE":
        record["spouse2_xref"] = value.strip()
    elif tag == "CHIL":
        record["children_xrefs"].append(value.strip())
    elif tag == "NOTE":
        record["notes"] = value.strip()


def _parse_fam_sub(
    record: Dict,
    parent_tag: Optional[str],
    tag: str,
    value: str,
) -> None:
    """Parse a level-2 tag inside a FAM record."""
    if parent_tag == "MARR":
        if tag == "DATE":
            record["marriage_date"] = _parse_date(value)
        elif tag == "PLAC":
            record["marriage_place"] = value.strip()
    elif parent_tag == "DIV":
        if tag == "DATE":
            record["divorce_date"] = _parse_date(value)

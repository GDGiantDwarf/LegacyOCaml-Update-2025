import json
import os
import sqlite3
from datetime import datetime, date

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from geneweb.core.database import BaseManager

router = APIRouter()


def _get_db_path(base_name: str):
    """Return the path to the database file."""
    return BaseManager.bases_dir() / f"{base_name}.db"


def _safe_connect(base_name: str):
    """Connect to DB or return None if missing."""
    db_path = _get_db_path(base_name)
    if not db_path.exists():
        return None
    return sqlite3.connect(str(db_path))


def _table_exists(con, table_name: str) -> bool:
    """Check if a table exists in the database."""
    cur = con.execute(
        "SELECT name FROM sqlite_master "
        "WHERE type='table' AND name=?",
        (table_name,),
    )
    return cur.fetchone() is not None


def _safe_count(con, table_name: str) -> int:
    """Count rows in a table, return 0 if missing."""
    if not _table_exists(con, table_name):
        return 0
    try:
        cur = con.execute(
            f"SELECT COUNT(*) FROM [{table_name}]"
        )
        return cur.fetchone()[0]
    except Exception:
        return 0


def _get_templates_and_lang(request: Request):
    """Extract templates, lang_manager, lang, etc."""
    templates = request.app.state.templates
    lang_manager = request.app.state.lang_manager
    lang = getattr(
        request.state,
        "lang",
        lang_manager.default_lang,
    )
    translations = (
        lang_manager.get_translations_for_lang(lang)
    )
    translations_json = json.dumps(
        translations, ensure_ascii=False
    )
    return templates, lang, translations_json


# --- STATISTICS ---
@router.get(
    "/base/{base_name}/stats",
    response_class=HTMLResponse,
)
async def base_stats(
    request: Request, base_name: str
):
    """Display statistics for a genealogical base."""
    templates, lang, translations_json = (
        _get_templates_and_lang(request)
    )

    stats = _compute_stats(base_name)

    context = templates.get_context(request)
    context.update(
        {
            "base_name": base_name,
            "stats": stats,
            "translations_json": translations_json,
            "lang": lang,
        }
    )
    return templates.TemplateResponse(
        request, "stats.html", context
    )


def _compute_stats(base_name: str) -> dict:
    """Compute all statistics for the base."""
    con = _safe_connect(base_name)
    if con is None:
        return {"error": "Database not found"}

    try:
        con.row_factory = sqlite3.Row
        s = {}

        # Counts
        s["persons"] = _safe_count(con, "persons")
        s["families"] = _safe_count(con, "families")
        s["events"] = _safe_count(con, "events")
        s["sources"] = _safe_count(con, "sources")
        s["notes"] = _safe_count(con, "notes")
        s["media"] = _safe_count(con, "media")

        # Gender distribution
        s["gender"] = {"M": 0, "F": 0, "U": 0}
        if _table_exists(con, "persons"):
            for row in con.execute(
                "SELECT gender, COUNT(*) as cnt "
                "FROM persons GROUP BY gender"
            ):
                g = (row[0] or "").upper()
                if g == "M":
                    s["gender"]["M"] = row[1]
                elif g == "F":
                    s["gender"]["F"] = row[1]
                else:
                    s["gender"]["U"] += row[1]

        # Oldest person (earliest birth date)
        s["oldest"] = None
        if _table_exists(con, "persons"):
            row = con.execute(
                "SELECT first_name, last_name, "
                "birth_date FROM persons "
                "WHERE birth_date IS NOT NULL "
                "AND birth_date != '' "
                "ORDER BY birth_date ASC LIMIT 1"
            ).fetchone()
            if row:
                s["oldest"] = {
                    "name": f"{row[0]} {row[1]}",
                    "date": row[2],
                }

        # Most recent person (latest birth date)
        s["most_recent"] = None
        if _table_exists(con, "persons"):
            row = con.execute(
                "SELECT first_name, last_name, "
                "birth_date FROM persons "
                "WHERE birth_date IS NOT NULL "
                "AND birth_date != '' "
                "ORDER BY birth_date DESC LIMIT 1"
            ).fetchone()
            if row:
                s["most_recent"] = {
                    "name": f"{row[0]} {row[1]}",
                    "date": row[2],
                }

        # Average lifespan
        s["avg_lifespan"] = None
        if _table_exists(con, "persons"):
            row = con.execute(
                "SELECT AVG("
                "  CAST("
                "    julianday(death_date) "
                "    - julianday(birth_date) "
                "  AS REAL) / 365.25"
                ") FROM persons "
                "WHERE birth_date IS NOT NULL "
                "AND birth_date != '' "
                "AND death_date IS NOT NULL "
                "AND death_date != ''"
            ).fetchone()
            if row and row[0] is not None:
                s["avg_lifespan"] = round(row[0], 1)

        # Top 10 surnames
        s["top_surnames"] = []
        if _table_exists(con, "persons"):
            rows = con.execute(
                "SELECT last_name, COUNT(*) as cnt "
                "FROM persons "
                "WHERE last_name IS NOT NULL "
                "AND last_name != '' "
                "GROUP BY last_name "
                "ORDER BY cnt DESC LIMIT 10"
            ).fetchall()
            s["top_surnames"] = [
                {"name": r[0], "count": r[1]}
                for r in rows
            ]

        # Top 10 firstnames
        s["top_firstnames"] = []
        if _table_exists(con, "persons"):
            rows = con.execute(
                "SELECT first_name, COUNT(*) as cnt "
                "FROM persons "
                "WHERE first_name IS NOT NULL "
                "AND first_name != '' "
                "GROUP BY first_name "
                "ORDER BY cnt DESC LIMIT 10"
            ).fetchall()
            s["top_firstnames"] = [
                {"name": r[0], "count": r[1]}
                for r in rows
            ]

        # Top 10 birth places
        s["top_birth_places"] = []
        if _table_exists(con, "persons"):
            rows = con.execute(
                "SELECT birth_place, "
                "COUNT(*) as cnt "
                "FROM persons "
                "WHERE birth_place IS NOT NULL "
                "AND birth_place != '' "
                "GROUP BY birth_place "
                "ORDER BY cnt DESC LIMIT 10"
            ).fetchall()
            s["top_birth_places"] = [
                {"name": r[0], "count": r[1]}
                for r in rows
            ]

        return s
    except Exception as e:
        return {"error": str(e)}
    finally:
        con.close()


# --- ANNIVERSARIES ---
@router.get(
    "/base/{base_name}/anniversaries",
    response_class=HTMLResponse,
)
async def base_anniversaries(
    request: Request, base_name: str
):
    """Display anniversaries for today/this month."""
    templates, lang, translations_json = (
        _get_templates_and_lang(request)
    )

    today = date.today()
    anniv = _compute_anniversaries(base_name, today)

    context = templates.get_context(request)
    context.update(
        {
            "base_name": base_name,
            "anniv": anniv,
            "today": today,
            "translations_json": translations_json,
            "lang": lang,
        }
    )
    return templates.TemplateResponse(
        request, "anniversaries.html", context
    )


def _date_like_patterns(month: int, day: int):
    """Return SQL LIKE patterns for various formats."""
    mm = f"{month:02d}"
    dd = f"{day:02d}"
    return [
        f"%-{mm}-{dd}",       # YYYY-MM-DD
        f"%-{mm}-{dd} %",     # YYYY-MM-DD HH:MM
        f"%/{mm}/{dd}",       # YYYY/MM/DD
        f"{dd}/{mm}/%",       # DD/MM/YYYY
        f"{dd}-{mm}-%",       # DD-MM-YYYY
    ]


def _month_like_patterns(month: int):
    """Return SQL LIKE patterns for a given month."""
    mm = f"{month:02d}"
    return [
        f"%-{mm}-%",          # YYYY-MM-DD
        f"%/{mm}/%",          # YYYY/MM/DD or DD/MM/YYYY
    ]


def _compute_anniversaries(
    base_name: str, today: date
) -> dict:
    """Compute birth/death/marriage anniversaries."""
    con = _safe_connect(base_name)
    if con is None:
        return {"error": "Database not found"}

    try:
        result = {
            "births_today": [],
            "deaths_today": [],
            "marriages_today": [],
            "births_month": [],
            "deaths_month": [],
            "marriages_month": [],
        }

        day_patterns = _date_like_patterns(
            today.month, today.day
        )
        month_patterns = _month_like_patterns(
            today.month
        )

        # --- Births today ---
        if _table_exists(con, "persons"):
            for pat in day_patterns:
                rows = con.execute(
                    "SELECT first_name, last_name, "
                    "birth_date FROM persons "
                    "WHERE birth_date LIKE ?",
                    (pat,),
                ).fetchall()
                for r in rows:
                    entry = {
                        "name": f"{r[0]} {r[1]}",
                        "date": r[2],
                    }
                    if entry not in (
                        result["births_today"]
                    ):
                        result["births_today"].append(
                            entry
                        )

        # --- Deaths today ---
        if _table_exists(con, "persons"):
            for pat in day_patterns:
                rows = con.execute(
                    "SELECT first_name, last_name, "
                    "death_date FROM persons "
                    "WHERE death_date LIKE ?",
                    (pat,),
                ).fetchall()
                for r in rows:
                    entry = {
                        "name": f"{r[0]} {r[1]}",
                        "date": r[2],
                    }
                    if entry not in (
                        result["deaths_today"]
                    ):
                        result["deaths_today"].append(
                            entry
                        )

        # --- Marriages today ---
        if _table_exists(con, "families"):
            has_persons = _table_exists(
                con, "persons"
            )
            for pat in day_patterns:
                if has_persons:
                    rows = con.execute(
                        "SELECT p1.first_name, "
                        "p1.last_name, "
                        "p2.first_name, "
                        "p2.last_name, "
                        "f.marriage_date "
                        "FROM families f "
                        "LEFT JOIN persons p1 "
                        "ON f.spouse1_id = p1.id "
                        "LEFT JOIN persons p2 "
                        "ON f.spouse2_id = p2.id "
                        "WHERE f.marriage_date "
                        "LIKE ?",
                        (pat,),
                    ).fetchall()
                    for r in rows:
                        s1 = f"{r[0] or ''} " \
                             f"{r[1] or ''}"
                        s2 = f"{r[2] or ''} " \
                             f"{r[3] or ''}"
                        entry = {
                            "couple": (
                                f"{s1.strip()} & "
                                f"{s2.strip()}"
                            ),
                            "date": r[4],
                        }
                        if entry not in (
                            result["marriages_today"]
                        ):
                            result[
                                "marriages_today"
                            ].append(entry)
                else:
                    rows = con.execute(
                        "SELECT spouse1_id, "
                        "spouse2_id, "
                        "marriage_date "
                        "FROM families "
                        "WHERE marriage_date LIKE ?",
                        (pat,),
                    ).fetchall()
                    for r in rows:
                        entry = {
                            "couple": (
                                f"#{r[0]} & #{r[1]}"
                            ),
                            "date": r[2],
                        }
                        if entry not in (
                            result["marriages_today"]
                        ):
                            result[
                                "marriages_today"
                            ].append(entry)

        # --- Births this month ---
        if _table_exists(con, "persons"):
            for pat in month_patterns:
                rows = con.execute(
                    "SELECT first_name, last_name, "
                    "birth_date FROM persons "
                    "WHERE birth_date LIKE ?",
                    (pat,),
                ).fetchall()
                for r in rows:
                    entry = {
                        "name": f"{r[0]} {r[1]}",
                        "date": r[2],
                    }
                    if entry not in (
                        result["births_month"]
                    ):
                        result[
                            "births_month"
                        ].append(entry)

        # --- Deaths this month ---
        if _table_exists(con, "persons"):
            for pat in month_patterns:
                rows = con.execute(
                    "SELECT first_name, last_name, "
                    "death_date FROM persons "
                    "WHERE death_date LIKE ?",
                    (pat,),
                ).fetchall()
                for r in rows:
                    entry = {
                        "name": f"{r[0]} {r[1]}",
                        "date": r[2],
                    }
                    if entry not in (
                        result["deaths_month"]
                    ):
                        result[
                            "deaths_month"
                        ].append(entry)

        # --- Marriages this month ---
        if _table_exists(con, "families"):
            has_persons = _table_exists(
                con, "persons"
            )
            for pat in month_patterns:
                if has_persons:
                    rows = con.execute(
                        "SELECT p1.first_name, "
                        "p1.last_name, "
                        "p2.first_name, "
                        "p2.last_name, "
                        "f.marriage_date "
                        "FROM families f "
                        "LEFT JOIN persons p1 "
                        "ON f.spouse1_id = p1.id "
                        "LEFT JOIN persons p2 "
                        "ON f.spouse2_id = p2.id "
                        "WHERE f.marriage_date "
                        "LIKE ?",
                        (pat,),
                    ).fetchall()
                    for r in rows:
                        s1 = f"{r[0] or ''} " \
                             f"{r[1] or ''}"
                        s2 = f"{r[2] or ''} " \
                             f"{r[3] or ''}"
                        entry = {
                            "couple": (
                                f"{s1.strip()} & "
                                f"{s2.strip()}"
                            ),
                            "date": r[4],
                        }
                        if entry not in (
                            result["marriages_month"]
                        ):
                            result[
                                "marriages_month"
                            ].append(entry)
                else:
                    rows = con.execute(
                        "SELECT spouse1_id, "
                        "spouse2_id, "
                        "marriage_date "
                        "FROM families "
                        "WHERE marriage_date LIKE ?",
                        (pat,),
                    ).fetchall()
                    for r in rows:
                        entry = {
                            "couple": (
                                f"#{r[0]} & #{r[1]}"
                            ),
                            "date": r[2],
                        }
                        if entry not in (
                            result["marriages_month"]
                        ):
                            result[
                                "marriages_month"
                            ].append(entry)

        return result
    except Exception as e:
        return {"error": str(e)}
    finally:
        con.close()


# --- PLACES / SURNAME ---
@router.get(
    "/base/{base_name}/places",
    response_class=HTMLResponse,
)
async def base_places(
    request: Request, base_name: str
):
    """Display places with associated surnames."""
    templates, lang, translations_json = (
        _get_templates_and_lang(request)
    )

    # Filter params
    bi = request.query_params.get("bi", "on")
    ba = request.query_params.get("ba", "on")
    ma = request.query_params.get("ma", "on")
    de = request.query_params.get("de", "on")
    bu = request.query_params.get("bu", "on")

    filters = {
        "bi": bi == "on",
        "ba": ba == "on",
        "ma": ma == "on",
        "de": de == "on",
        "bu": bu == "on",
    }

    places = _compute_places(base_name, filters)

    context = templates.get_context(request)
    context.update(
        {
            "base_name": base_name,
            "places": places,
            "filters": filters,
            "translations_json": translations_json,
            "lang": lang,
        }
    )
    return templates.TemplateResponse(
        request, "places.html", context
    )


def _compute_places(
    base_name: str, filters: dict
) -> list:
    """Compute places with associated surnames."""
    con = _safe_connect(base_name)
    if con is None:
        return []

    try:
        place_surnames = {}

        has_persons = _table_exists(con, "persons")
        has_families = _table_exists(con, "families")
        has_events = _table_exists(con, "events")

        # Birth places
        if filters.get("bi") and has_persons:
            rows = con.execute(
                "SELECT birth_place, last_name "
                "FROM persons "
                "WHERE birth_place IS NOT NULL "
                "AND birth_place != '' "
                "AND last_name IS NOT NULL "
                "AND last_name != ''"
            ).fetchall()
            for r in rows:
                place = r[0]
                surname = r[1]
                if place not in place_surnames:
                    place_surnames[place] = {
                        "surnames": set(),
                        "types": set(),
                    }
                place_surnames[place][
                    "surnames"
                ].add(surname)
                place_surnames[place][
                    "types"
                ].add("birth")

        # Baptism places (from events)
        if filters.get("ba") and has_events:
            if has_persons:
                rows = con.execute(
                    "SELECT e.place, p.last_name "
                    "FROM events e "
                    "JOIN persons p "
                    "ON e.person_id = p.id "
                    "WHERE e.event_type = 'baptism' "
                    "AND e.place IS NOT NULL "
                    "AND e.place != '' "
                    "AND p.last_name IS NOT NULL "
                    "AND p.last_name != ''"
                ).fetchall()
                for r in rows:
                    place = r[0]
                    surname = r[1]
                    if place not in place_surnames:
                        place_surnames[place] = {
                            "surnames": set(),
                            "types": set(),
                        }
                    place_surnames[place][
                        "surnames"
                    ].add(surname)
                    place_surnames[place][
                        "types"
                    ].add("baptism")

        # Death places
        if filters.get("de") and has_persons:
            rows = con.execute(
                "SELECT death_place, last_name "
                "FROM persons "
                "WHERE death_place IS NOT NULL "
                "AND death_place != '' "
                "AND last_name IS NOT NULL "
                "AND last_name != ''"
            ).fetchall()
            for r in rows:
                place = r[0]
                surname = r[1]
                if place not in place_surnames:
                    place_surnames[place] = {
                        "surnames": set(),
                        "types": set(),
                    }
                place_surnames[place][
                    "surnames"
                ].add(surname)
                place_surnames[place][
                    "types"
                ].add("death")

        # Marriage places
        if filters.get("ma") and has_families:
            if has_persons:
                rows = con.execute(
                    "SELECT f.marriage_place, "
                    "p1.last_name, p2.last_name "
                    "FROM families f "
                    "LEFT JOIN persons p1 "
                    "ON f.spouse1_id = p1.id "
                    "LEFT JOIN persons p2 "
                    "ON f.spouse2_id = p2.id "
                    "WHERE f.marriage_place "
                    "IS NOT NULL "
                    "AND f.marriage_place != ''"
                ).fetchall()
                for r in rows:
                    place = r[0]
                    if place not in place_surnames:
                        place_surnames[place] = {
                            "surnames": set(),
                            "types": set(),
                        }
                    if r[1]:
                        place_surnames[place][
                            "surnames"
                        ].add(r[1])
                    if r[2]:
                        place_surnames[place][
                            "surnames"
                        ].add(r[2])
                    place_surnames[place][
                        "types"
                    ].add("marriage")

        # Burial places (from events)
        if filters.get("bu") and has_events:
            if has_persons:
                rows = con.execute(
                    "SELECT e.place, p.last_name "
                    "FROM events e "
                    "JOIN persons p "
                    "ON e.person_id = p.id "
                    "WHERE e.event_type = 'burial' "
                    "AND e.place IS NOT NULL "
                    "AND e.place != '' "
                    "AND p.last_name IS NOT NULL "
                    "AND p.last_name != ''"
                ).fetchall()
                for r in rows:
                    place = r[0]
                    surname = r[1]
                    if place not in place_surnames:
                        place_surnames[place] = {
                            "surnames": set(),
                            "types": set(),
                        }
                    place_surnames[place][
                        "surnames"
                    ].add(surname)
                    place_surnames[place][
                        "types"
                    ].add("burial")

        # Convert sets to sorted lists
        result = []
        for place in sorted(place_surnames.keys()):
            result.append(
                {
                    "place": place,
                    "surnames": sorted(
                        place_surnames[place][
                            "surnames"
                        ]
                    ),
                    "types": sorted(
                        place_surnames[place]["types"]
                    ),
                    "count": len(
                        place_surnames[place][
                            "surnames"
                        ]
                    ),
                }
            )
        return result
    except Exception:
        return []
    finally:
        con.close()


# --- CONFIGURATION ---
@router.get(
    "/base/{base_name}/config",
    response_class=HTMLResponse,
)
async def base_config_get(
    request: Request, base_name: str
):
    """Display database configuration."""
    templates, lang, translations_json = (
        _get_templates_and_lang(request)
    )

    config = _compute_config(base_name)

    context = templates.get_context(request)
    context.update(
        {
            "base_name": base_name,
            "config": config,
            "translations_json": translations_json,
            "lang": lang,
        }
    )
    return templates.TemplateResponse(
        request, "config.html", context
    )


@router.post(
    "/base/{base_name}/config",
    response_class=HTMLResponse,
)
async def base_config_post(
    request: Request, base_name: str
):
    """Handle config changes (currently read-only)."""
    return await base_config_get(request, base_name)


def _compute_config(base_name: str) -> dict:
    """Compute database configuration metadata."""
    db_path = _get_db_path(base_name)
    config = {
        "name": base_name,
        "path": str(db_path),
        "exists": db_path.exists(),
        "size": 0,
        "size_human": "0 B",
        "last_modified": None,
        "tables": {},
        "error": None,
    }

    if not db_path.exists():
        config["error"] = "Database not found"
        return config

    try:
        stat = os.stat(str(db_path))
        config["size"] = stat.st_size
        config["size_human"] = _human_size(
            stat.st_size
        )
        config["last_modified"] = (
            datetime.fromtimestamp(
                stat.st_mtime
            ).strftime("%Y-%m-%d %H:%M:%S")
        )
    except Exception:
        pass

    con = _safe_connect(base_name)
    if con is None:
        config["error"] = "Cannot connect"
        return config

    try:
        # List all tables and their row counts
        tables = con.execute(
            "SELECT name FROM sqlite_master "
            "WHERE type='table' "
            "ORDER BY name"
        ).fetchall()
        for row in tables:
            tname = row[0]
            try:
                cnt = con.execute(
                    f"SELECT COUNT(*) "
                    f"FROM [{tname}]"
                ).fetchone()[0]
                config["tables"][tname] = cnt
            except Exception:
                config["tables"][tname] = "?"
    except Exception as e:
        config["error"] = str(e)
    finally:
        con.close()

    return config


def _human_size(size_bytes: int) -> str:
    """Convert bytes to human-readable string."""
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    elif size_bytes < 1024 * 1024 * 1024:
        return f"{size_bytes / (1024 * 1024):.1f} MB"
    else:
        val = size_bytes / (1024 * 1024 * 1024)
        return f"{val:.1f} GB"

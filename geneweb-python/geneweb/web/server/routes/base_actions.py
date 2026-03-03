"""
Route handler for /base/{base_name} with all ?m= actions.

Replaces the former base_detail.py route and adds support
for search (?m=S), surname list (?m=N), firstname list
(?m=P), titles (?m=TT), advanced search (?m=AS), and
individual view (?i=).
"""

import json
import sqlite3
from pathlib import Path

from fastapi import APIRouter, Request, Query
from fastapi.responses import HTMLResponse

from geneweb.core.database import BaseManager

router = APIRouter()


# ----------------------------------------------------------
# Helpers
# ----------------------------------------------------------

def _get_db_path(base_name: str) -> Path:
    """Return the path to the SQLite DB for *base_name*."""
    return BaseManager.bases_dir() / f"{base_name}.db"


def _get_connection(base_name: str):
    """Open a read-only sqlite3 connection (or None)."""
    path = _get_db_path(base_name)
    if not path.exists():
        return None
    conn = sqlite3.connect(str(path))
    conn.row_factory = sqlite3.Row
    return conn


def _person_count(base_name: str) -> int:
    """Return the number of persons in *base_name*."""
    conn = _get_connection(base_name)
    if conn is None:
        return 0
    try:
        cur = conn.execute(
            "SELECT COUNT(*) FROM persons"
        )
        return cur.fetchone()[0]
    except Exception:
        return 0
    finally:
        conn.close()


def _ctx(request: Request, extra: dict | None = None):
    """Build the base Jinja2 context dict."""
    templates = request.app.state.templates
    ctx = templates.get_context(request)
    if extra:
        ctx.update(extra)
    return ctx


def _tpl(request: Request):
    """Shortcut to get the templates object."""
    return request.app.state.templates


# ----------------------------------------------------------
# Main route
# ----------------------------------------------------------

@router.get(
    "/base/{base_name}", response_class=HTMLResponse
)
async def base_action(
    request: Request,
    base_name: str,
    m: str = Query(None),
    n: str = Query(""),
    p: str = Query(""),
    tri: str = Query("A"),
    t: str = Query(""),
    data: str = Query(""),
    i: str = Query(""),
    v: str = Query(""),
    # Advanced search fields
    birth_place: str = Query(""),
    death_place: str = Query(""),
    occu: str = Query(""),
    birth_y1: str = Query(""),
    birth_y2: str = Query(""),
):
    """Dispatch to the correct sub-handler."""

    if m is None and not i:
        return _render_base_details(request, base_name)

    if i:
        return _render_individual(
            request, base_name, i
        )

    handlers = {
        "S": lambda: _search(
            request, base_name, n, p,
            birth_place, death_place, occu,
            birth_y1, birth_y2,
        ),
        "N": lambda: _surname_list(
            request, base_name, tri
        ),
        "P": lambda: _firstname_list(
            request, base_name, tri
        ),
        "TT": lambda: _titles_list(
            request, base_name, t, p
        ),
        "AS": lambda: _advanced_search(
            request, base_name
        ),
    }

    handler = handlers.get(m)
    if handler:
        return handler()

    return _render_base_details(request, base_name)


# ----------------------------------------------------------
# Existing base_details (ported from base_detail.py)
# ----------------------------------------------------------

def _render_base_details(request, base_name):
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
    count = _person_count(base_name)

    context = _ctx(request, {
        "base_name": base_name,
        "person_count": count,
        "translations_json": translations_json,
        "lang": lang,
    })
    return _tpl(request).TemplateResponse(
        request, "base_details.html", context
    )


# ----------------------------------------------------------
# ?m=S  --  Search persons
# ----------------------------------------------------------

def _search(
    request, base_name, surname, firstname,
    birth_place="", death_place="", occu="",
    birth_y1="", birth_y2="",
):
    conn = _get_connection(base_name)
    results = []
    if conn is not None:
        try:
            clauses = []
            params = []

            if surname:
                clauses.append(
                    "last_name LIKE ? COLLATE NOCASE"
                )
                params.append(f"%{surname}%")
            if firstname:
                clauses.append(
                    "first_name LIKE ? COLLATE NOCASE"
                )
                params.append(f"%{firstname}%")
            if birth_place:
                clauses.append(
                    "birth_place LIKE ? COLLATE NOCASE"
                )
                params.append(f"%{birth_place}%")
            if death_place:
                clauses.append(
                    "death_place LIKE ? COLLATE NOCASE"
                )
                params.append(f"%{death_place}%")
            if occu:
                clauses.append(
                    "occupation LIKE ? COLLATE NOCASE"
                )
                params.append(f"%{occu}%")
            if birth_y1:
                clauses.append(
                    "birth_date >= ?"
                )
                params.append(f"{birth_y1}-01-01")
            if birth_y2:
                clauses.append(
                    "birth_date <= ?"
                )
                params.append(f"{birth_y2}-12-31")

            where = (
                "WHERE " + " AND ".join(clauses)
                if clauses else ""
            )
            sql = (
                "SELECT id, first_name, last_name,"
                " birth_date, death_date, gender,"
                " occupation"
                f" FROM persons {where}"
                " ORDER BY last_name, first_name"
                " LIMIT 500"
            )
            cur = conn.execute(sql, params)
            results = [dict(r) for r in cur.fetchall()]
        except Exception:
            results = []
        finally:
            conn.close()

    context = _ctx(request, {
        "base_name": base_name,
        "results": results,
        "surname": surname,
        "firstname": firstname,
        "result_count": len(results),
    })
    return _tpl(request).TemplateResponse(
        request, "search_results.html", context
    )


# ----------------------------------------------------------
# ?m=N  --  Surname list
# ----------------------------------------------------------

def _surname_list(request, base_name, tri):
    conn = _get_connection(base_name)
    items = []
    if conn is not None:
        try:
            order = (
                "cnt DESC, last_name"
                if tri == "F"
                else "last_name"
            )
            sql = (
                "SELECT last_name, COUNT(*) AS cnt"
                " FROM persons"
                " WHERE last_name != ''"
                f" GROUP BY last_name ORDER BY {order}"
            )
            cur = conn.execute(sql)
            items = [dict(r) for r in cur.fetchall()]
        except Exception:
            items = []
        finally:
            conn.close()

    context = _ctx(request, {
        "base_name": base_name,
        "items": items,
        "tri": tri,
        "total": sum(it["cnt"] for it in items),
    })
    return _tpl(request).TemplateResponse(
        request, "surname_list.html", context
    )


# ----------------------------------------------------------
# ?m=P  --  First-name list
# ----------------------------------------------------------

def _firstname_list(request, base_name, tri):
    conn = _get_connection(base_name)
    items = []
    if conn is not None:
        try:
            order = (
                "cnt DESC, first_name"
                if tri == "F"
                else "first_name"
            )
            sql = (
                "SELECT first_name, COUNT(*) AS cnt"
                " FROM persons"
                " WHERE first_name != ''"
                f" GROUP BY first_name ORDER BY {order}"
            )
            cur = conn.execute(sql)
            items = [dict(r) for r in cur.fetchall()]
        except Exception:
            items = []
        finally:
            conn.close()

    context = _ctx(request, {
        "base_name": base_name,
        "items": items,
        "tri": tri,
        "total": sum(it["cnt"] for it in items),
    })
    return _tpl(request).TemplateResponse(
        request, "firstname_list.html", context
    )


# ----------------------------------------------------------
# ?m=TT  --  Titles / occupations list
# ----------------------------------------------------------

def _titles_list(request, base_name, title, fief):
    conn = _get_connection(base_name)
    items = []
    persons = []
    mode = "list"

    if conn is not None:
        try:
            if title or fief:
                mode = "detail"
                clauses = []
                params = []
                if title:
                    clauses.append(
                        "occupation LIKE ?"
                        " COLLATE NOCASE"
                    )
                    params.append(f"%{title}%")
                if fief and fief != "*":
                    clauses.append(
                        "(birth_place LIKE ?"
                        " COLLATE NOCASE"
                        " OR death_place LIKE ?"
                        " COLLATE NOCASE)"
                    )
                    params.append(f"%{fief}%")
                    params.append(f"%{fief}%")
                where = (
                    "WHERE " + " AND ".join(clauses)
                    if clauses else ""
                )
                sql = (
                    "SELECT id, first_name, last_name,"
                    " occupation, birth_place,"
                    " death_place"
                    f" FROM persons {where}"
                    " ORDER BY last_name, first_name"
                )
                cur = conn.execute(sql, params)
                persons = [
                    dict(r) for r in cur.fetchall()
                ]
            else:
                sql = (
                    "SELECT occupation,"
                    " COUNT(*) AS cnt"
                    " FROM persons"
                    " WHERE occupation IS NOT NULL"
                    " AND occupation != ''"
                    " GROUP BY occupation"
                    " ORDER BY occupation"
                )
                cur = conn.execute(sql)
                items = [
                    dict(r) for r in cur.fetchall()
                ]
        except Exception:
            items = []
            persons = []
        finally:
            conn.close()

    context = _ctx(request, {
        "base_name": base_name,
        "items": items,
        "persons": persons,
        "mode": mode,
        "title_q": title,
        "fief_q": fief,
    })
    return _tpl(request).TemplateResponse(
        request, "titles_list.html", context
    )


# ----------------------------------------------------------
# ?m=AS  --  Advanced search form
# ----------------------------------------------------------

def _advanced_search(request, base_name):
    context = _ctx(request, {
        "base_name": base_name,
    })
    return _tpl(request).TemplateResponse(
        request, "advanced_search.html", context
    )


# ----------------------------------------------------------
# ?i=  --  Individual detail page
# ----------------------------------------------------------

def _render_individual(request, base_name, pid):
    conn = _get_connection(base_name)
    person = None
    families = []
    children = []
    events = []
    parents_family = None
    father = None
    mother = None

    if conn is not None:
        try:
            # Handle "random" pseudo-id
            if pid == "random":
                cur = conn.execute(
                    "SELECT id FROM persons"
                    " ORDER BY RANDOM() LIMIT 1"
                )
                row = cur.fetchone()
                if row is None:
                    pid = "0"
                else:
                    pid = str(row["id"])

            # Fetch person
            cur = conn.execute(
                "SELECT * FROM persons WHERE id = ?",
                (int(pid),),
            )
            row = cur.fetchone()
            if row:
                person = dict(row)

            if person:
                person_id = person["id"]

                # Families as spouse
                sql_fam = (
                    "SELECT f.*, "
                    " s1.first_name AS s1_fn,"
                    " s1.last_name AS s1_ln,"
                    " s1.id AS s1_id,"
                    " s2.first_name AS s2_fn,"
                    " s2.last_name AS s2_ln,"
                    " s2.id AS s2_id"
                    " FROM families f"
                    " LEFT JOIN persons s1"
                    "   ON f.spouse1_id = s1.id"
                    " LEFT JOIN persons s2"
                    "   ON f.spouse2_id = s2.id"
                    " WHERE f.spouse1_id = ?"
                    "    OR f.spouse2_id = ?"
                )
                cur = conn.execute(
                    sql_fam, (person_id, person_id)
                )
                families = [
                    dict(r) for r in cur.fetchall()
                ]

                # Children
                for fam in families:
                    sql_ch = (
                        "SELECT p.id, p.first_name,"
                        " p.last_name, p.birth_date,"
                        " p.gender"
                        " FROM children_in_family c"
                        " JOIN persons p"
                        "   ON c.person_id = p.id"
                        " WHERE c.family_id = ?"
                        " ORDER BY p.birth_date"
                    )
                    cur = conn.execute(
                        sql_ch, (fam["id"],)
                    )
                    fam_children = [
                        dict(r) for r in cur.fetchall()
                    ]
                    children.extend(fam_children)

                # Parents (family where person is child)
                sql_par = (
                    "SELECT f.*,"
                    " s1.first_name AS s1_fn,"
                    " s1.last_name AS s1_ln,"
                    " s1.id AS s1_id,"
                    " s2.first_name AS s2_fn,"
                    " s2.last_name AS s2_ln,"
                    " s2.id AS s2_id"
                    " FROM children_in_family c"
                    " JOIN families f"
                    "   ON c.family_id = f.id"
                    " LEFT JOIN persons s1"
                    "   ON f.spouse1_id = s1.id"
                    " LEFT JOIN persons s2"
                    "   ON f.spouse2_id = s2.id"
                    " WHERE c.person_id = ?"
                )
                cur = conn.execute(
                    sql_par, (person_id,)
                )
                row = cur.fetchone()
                if row:
                    parents_family = dict(row)
                    if parents_family.get("s1_id"):
                        father = {
                            "id": parents_family["s1_id"],
                            "first_name": (
                                parents_family["s1_fn"]
                            ),
                            "last_name": (
                                parents_family["s1_ln"]
                            ),
                        }
                    if parents_family.get("s2_id"):
                        mother = {
                            "id": parents_family["s2_id"],
                            "first_name": (
                                parents_family["s2_fn"]
                            ),
                            "last_name": (
                                parents_family["s2_ln"]
                            ),
                        }

                # Events
                sql_ev = (
                    "SELECT * FROM events"
                    " WHERE person_id = ?"
                    " ORDER BY date"
                )
                cur = conn.execute(
                    sql_ev, (person_id,)
                )
                events = [
                    dict(r) for r in cur.fetchall()
                ]
        except Exception:
            person = None
        finally:
            conn.close()

    context = _ctx(request, {
        "base_name": base_name,
        "person": person,
        "families": families,
        "children": children,
        "events": events,
        "father": father,
        "mother": mother,
    })
    return _tpl(request).TemplateResponse(
        request, "individual.html", context
    )

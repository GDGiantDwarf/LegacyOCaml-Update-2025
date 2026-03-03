"""Routes for data management: Add Family, Notes, Books."""

import json
import sqlite3

from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse

from geneweb.core.database import BaseManager

router = APIRouter()


def _get_db_path(base_name: str):
    """Return the path to the database file."""
    return BaseManager.bases_dir() / f"{base_name}.db"


def _base_exists(base_name: str) -> bool:
    """Check if a base database exists."""
    return _get_db_path(base_name).exists()


def _get_conn(base_name: str):
    """Open a sqlite3 connection to the base."""
    db_path = _get_db_path(base_name)
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    return conn


def _build_context(request: Request, base_name: str):
    """Build the standard template context."""
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
    context = templates.get_context(request)
    context.update({
        "base_name": base_name,
        "translations_json": translations_json,
        "lang": lang,
    })
    return context


# ============================================================
# ADD FAMILY
# ============================================================

@router.get(
    "/base/{base_name}/add-family",
    response_class=HTMLResponse,
)
async def add_family_form(
    request: Request, base_name: str
):
    """Display the add family form."""
    if not _base_exists(base_name):
        return HTMLResponse(
            content="Base not found", status_code=404
        )
    templates = request.app.state.templates
    context = _build_context(request, base_name)

    # Fetch existing persons for optional dropdowns
    persons = []
    try:
        conn = _get_conn(base_name)
        cur = conn.execute(
            "SELECT id, first_name, last_name "
            "FROM persons ORDER BY last_name, first_name"
        )
        persons = [dict(r) for r in cur.fetchall()]
        conn.close()
    except Exception:
        pass

    context["persons"] = persons
    context["success"] = request.query_params.get(
        "success", ""
    )
    return templates.TemplateResponse(
        request, "add_family.html", context
    )


@router.post(
    "/base/{base_name}/add-family",
    response_class=HTMLResponse,
)
async def add_family_submit(
    request: Request, base_name: str
):
    """Create a family with spouses and children."""
    if not _base_exists(base_name):
        return HTMLResponse(
            content="Base not found", status_code=404
        )

    form = await request.form()
    conn = _get_conn(base_name)
    try:
        # --- Spouse 1 ---
        cur1 = conn.execute(
            "INSERT INTO persons "
            "(first_name, last_name, gender, "
            "birth_date, birth_place) "
            "VALUES (?, ?, ?, ?, ?)",
            (
                form.get("sp1_first_name", ""),
                form.get("sp1_last_name", ""),
                form.get("sp1_gender", "M"),
                form.get("sp1_birth_date") or None,
                form.get("sp1_birth_place") or None,
            ),
        )
        sp1_id = cur1.lastrowid

        # --- Spouse 2 ---
        cur2 = conn.execute(
            "INSERT INTO persons "
            "(first_name, last_name, gender, "
            "birth_date, birth_place) "
            "VALUES (?, ?, ?, ?, ?)",
            (
                form.get("sp2_first_name", ""),
                form.get("sp2_last_name", ""),
                form.get("sp2_gender", "F"),
                form.get("sp2_birth_date") or None,
                form.get("sp2_birth_place") or None,
            ),
        )
        sp2_id = cur2.lastrowid

        # --- Family ---
        cur_fam = conn.execute(
            "INSERT INTO families "
            "(spouse1_id, spouse2_id, "
            "marriage_date, marriage_place) "
            "VALUES (?, ?, ?, ?)",
            (
                sp1_id,
                sp2_id,
                form.get("marriage_date") or None,
                form.get("marriage_place") or None,
            ),
        )
        fam_id = cur_fam.lastrowid

        # --- Children ---
        idx = 0
        while True:
            c_fn = form.get(f"child_{idx}_first_name")
            c_ln = form.get(f"child_{idx}_last_name")
            if c_fn is None and c_ln is None:
                break
            if c_fn or c_ln:
                cur_c = conn.execute(
                    "INSERT INTO persons "
                    "(first_name, last_name, gender, "
                    "birth_date) "
                    "VALUES (?, ?, ?, ?)",
                    (
                        c_fn or "",
                        c_ln or "",
                        form.get(
                            f"child_{idx}_gender"
                        ) or None,
                        form.get(
                            f"child_{idx}_birth_date"
                        ) or None,
                    ),
                )
                child_id = cur_c.lastrowid
                conn.execute(
                    "INSERT INTO children_in_family "
                    "(person_id, family_id) "
                    "VALUES (?, ?)",
                    (child_id, fam_id),
                )
            idx += 1

        conn.commit()
    except Exception as exc:
        conn.rollback()
        conn.close()
        templates = request.app.state.templates
        context = _build_context(request, base_name)
        context["error"] = str(exc)
        context["persons"] = []
        return templates.TemplateResponse(
            request, "add_family.html", context
        )
    finally:
        if conn:
            conn.close()

    return RedirectResponse(
        url=(
            f"/base/{base_name}/add-family"
            f"?success=1"
        ),
        status_code=303,
    )


# ============================================================
# NOTES
# ============================================================

@router.get(
    "/base/{base_name}/notes",
    response_class=HTMLResponse,
)
async def notes_list(
    request: Request, base_name: str
):
    """Display all notes and form to add a new one."""
    if not _base_exists(base_name):
        return HTMLResponse(
            content="Base not found", status_code=404
        )
    templates = request.app.state.templates
    context = _build_context(request, base_name)

    notes = []
    persons = []
    try:
        conn = _get_conn(base_name)
        cur = conn.execute(
            "SELECT n.id, n.content, n.person_id, "
            "p.first_name, p.last_name "
            "FROM notes n "
            "LEFT JOIN persons p "
            "ON n.person_id = p.id "
            "ORDER BY n.id DESC"
        )
        notes = [dict(r) for r in cur.fetchall()]

        cur_p = conn.execute(
            "SELECT id, first_name, last_name "
            "FROM persons ORDER BY last_name, first_name"
        )
        persons = [dict(r) for r in cur_p.fetchall()]
        conn.close()
    except Exception:
        pass

    context["notes"] = notes
    context["persons"] = persons
    context["success"] = request.query_params.get(
        "success", ""
    )
    return templates.TemplateResponse(
        request, "notes.html", context
    )


@router.post(
    "/base/{base_name}/notes",
    response_class=HTMLResponse,
)
async def notes_submit(
    request: Request, base_name: str
):
    """Create or update a note."""
    if not _base_exists(base_name):
        return HTMLResponse(
            content="Base not found", status_code=404
        )

    form = await request.form()
    content = form.get("content", "").strip()
    person_id = form.get("person_id") or None
    note_id = form.get("note_id") or None

    if not content:
        return RedirectResponse(
            url=f"/base/{base_name}/notes",
            status_code=303,
        )

    if person_id:
        try:
            person_id = int(person_id)
        except (ValueError, TypeError):
            person_id = None

    conn = _get_conn(base_name)
    try:
        if note_id:
            conn.execute(
                "UPDATE notes SET content = ?, "
                "person_id = ? WHERE id = ?",
                (content, person_id, int(note_id)),
            )
        else:
            conn.execute(
                "INSERT INTO notes "
                "(content, person_id) VALUES (?, ?)",
                (content, person_id),
            )
        conn.commit()
    except Exception:
        conn.rollback()
    finally:
        conn.close()

    return RedirectResponse(
        url=f"/base/{base_name}/notes?success=1",
        status_code=303,
    )


# ============================================================
# BOOKS (fn, sn, place, occu, src)
# ============================================================

_BOOK_TITLES = {
    "fn": "First Names Book",
    "sn": "Surnames Book",
    "place": "Places Book",
    "occu": "Occupations Book",
    "src": "Sources Book",
}

_BOOK_ICONS = {
    "fn": "fa-child",
    "sn": "fa-signature",
    "place": "fa-map-location-dot",
    "occu": "fa-user-doctor",
    "src": "fa-box-archive",
}


def _fetch_book_data(conn, data_type: str):
    """Return rows for the given book type."""
    if data_type == "fn":
        cur = conn.execute(
            "SELECT first_name AS value, "
            "COUNT(*) AS cnt "
            "FROM persons "
            "WHERE first_name IS NOT NULL "
            "AND first_name != '' "
            "GROUP BY first_name "
            "ORDER BY first_name"
        )
    elif data_type == "sn":
        cur = conn.execute(
            "SELECT last_name AS value, "
            "COUNT(*) AS cnt "
            "FROM persons "
            "WHERE last_name IS NOT NULL "
            "AND last_name != '' "
            "GROUP BY last_name "
            "ORDER BY last_name"
        )
    elif data_type == "place":
        cur = conn.execute(
            "SELECT value, COUNT(*) AS cnt FROM ("
            "  SELECT birth_place AS value "
            "  FROM persons "
            "  WHERE birth_place IS NOT NULL "
            "  AND birth_place != '' "
            "  UNION ALL "
            "  SELECT death_place AS value "
            "  FROM persons "
            "  WHERE death_place IS NOT NULL "
            "  AND death_place != '' "
            ") GROUP BY value ORDER BY value"
        )
    elif data_type == "occu":
        cur = conn.execute(
            "SELECT occupation AS value, "
            "COUNT(*) AS cnt "
            "FROM persons "
            "WHERE occupation IS NOT NULL "
            "AND occupation != '' "
            "GROUP BY occupation "
            "ORDER BY occupation"
        )
    elif data_type == "src":
        cur = conn.execute(
            "SELECT id, title AS value, "
            "reference, type, repository, notes "
            "FROM sources ORDER BY title"
        )
    else:
        return []
    return [dict(r) for r in cur.fetchall()]


@router.get(
    "/base/{base_name}/book/{data_type}",
    response_class=HTMLResponse,
)
async def book_list(
    request: Request,
    base_name: str,
    data_type: str,
):
    """Display a book (list of data entries)."""
    if not _base_exists(base_name):
        return HTMLResponse(
            content="Base not found", status_code=404
        )
    if data_type not in _BOOK_TITLES:
        return HTMLResponse(
            content="Invalid data type",
            status_code=400,
        )

    templates = request.app.state.templates
    context = _build_context(request, base_name)

    rows = []
    try:
        conn = _get_conn(base_name)
        rows = _fetch_book_data(conn, data_type)
        conn.close()
    except Exception:
        pass

    context["rows"] = rows
    context["data_type"] = data_type
    context["book_title"] = _BOOK_TITLES[data_type]
    context["book_icon"] = _BOOK_ICONS[data_type]
    context["is_source"] = data_type == "src"
    context["success"] = request.query_params.get(
        "success", ""
    )
    return templates.TemplateResponse(
        request, "book.html", context
    )


@router.post(
    "/base/{base_name}/book/{data_type}",
    response_class=HTMLResponse,
)
async def book_submit(
    request: Request,
    base_name: str,
    data_type: str,
):
    """Add or edit a book entry."""
    if not _base_exists(base_name):
        return HTMLResponse(
            content="Base not found", status_code=404
        )
    if data_type not in _BOOK_TITLES:
        return HTMLResponse(
            content="Invalid data type",
            status_code=400,
        )

    form = await request.form()
    conn = _get_conn(base_name)

    try:
        if data_type == "src":
            title = form.get("title", "").strip()
            reference = form.get(
                "reference", ""
            ).strip()
            src_type = form.get("type", "").strip()
            repository = (
                form.get("repository", "").strip()
                or None
            )
            notes = (
                form.get("notes", "").strip() or None
            )
            src_id = form.get("source_id") or None

            if not title or not reference or not src_type:
                conn.close()
                return RedirectResponse(
                    url=(
                        f"/base/{base_name}"
                        f"/book/{data_type}"
                    ),
                    status_code=303,
                )

            if src_id:
                conn.execute(
                    "UPDATE sources SET title = ?, "
                    "reference = ?, type = ?, "
                    "repository = ?, notes = ? "
                    "WHERE id = ?",
                    (
                        title, reference, src_type,
                        repository, notes, int(src_id),
                    ),
                )
            else:
                conn.execute(
                    "INSERT INTO sources "
                    "(title, reference, type, "
                    "repository, notes) "
                    "VALUES (?, ?, ?, ?, ?)",
                    (
                        title, reference, src_type,
                        repository, notes,
                    ),
                )
        else:
            old_val = form.get("old_value", "").strip()
            new_val = form.get("new_value", "").strip()
            if not new_val:
                conn.close()
                return RedirectResponse(
                    url=(
                        f"/base/{base_name}"
                        f"/book/{data_type}"
                    ),
                    status_code=303,
                )

            col_map = {
                "fn": "first_name",
                "sn": "last_name",
                "place": None,
                "occu": "occupation",
            }

            if data_type == "place":
                if old_val:
                    conn.execute(
                        "UPDATE persons "
                        "SET birth_place = ? "
                        "WHERE birth_place = ?",
                        (new_val, old_val),
                    )
                    conn.execute(
                        "UPDATE persons "
                        "SET death_place = ? "
                        "WHERE death_place = ?",
                        (new_val, old_val),
                    )
            else:
                col = col_map.get(data_type)
                if col and old_val:
                    conn.execute(
                        f"UPDATE persons "
                        f"SET {col} = ? "
                        f"WHERE {col} = ?",
                        (new_val, old_val),
                    )

        conn.commit()
    except Exception:
        conn.rollback()
    finally:
        conn.close()

    return RedirectResponse(
        url=(
            f"/base/{base_name}"
            f"/book/{data_type}?success=1"
        ),
        status_code=303,
    )

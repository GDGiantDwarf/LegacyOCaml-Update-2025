# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Epitech project modernizing a legacy OCaml genealogy application (GeneWeb) into Python. The repo contains two codebases:

- **`Legacy/`** — Reference Flask implementation (the target feature set to match)
- **`geneweb-python/`** — Active FastAPI implementation (the code being developed)

The goal is to bring `geneweb-python` to feature parity with `Legacy`, then deploy via Terraform on Render.

## Build & Run Commands

All commands are run from repo root via Makefile:

```bash
make dependencies        # pip install -r geneweb-python/requirements.txt
make test                # pytest with coverage (all tests)
make build               # Docker compose up --build (gwd + gwsetup)
make audit               # pip-audit for vulnerability scanning
make conventions         # pycodestyle PEP8 check
make clean               # Stop containers + remove __pycache__, .pytest_cache, .coverage
make fclean              # clean + remove Docker images
make re                  # fclean + all
make admin ARGS="..."    # Launch gwsetup (admin, port 2316)
make user ARGS="..."     # Launch gwd (public, port 2317)
make all                 # Full pipeline: dependencies → audit → conventions → test → build
```

### Running a single test

```bash
cd geneweb-python && pytest tests/path/to/test_file.py -v
cd geneweb-python && pytest tests/path/to/test_file.py::TestClass::test_method -v
```

Note: `pytest.ini` sets `pythonpath = .` so imports resolve from `geneweb-python/`.

## Architecture — geneweb-python

### Two FastAPI Servers

| Server | Module | Port | Purpose |
|--------|--------|------|---------|
| **gwd** | `geneweb.gwd` | 2317 | Public genealogy browsing |
| **gwsetup** | `geneweb.gwsetup` | 2316 | Admin database management |

Both use uvicorn and accept CLI args via `geneweb/cli/parser_gwd.py` and `parser_gwsetup.py`.

### Layered Architecture

```
CLI (cli/)  →  Web Layer (web/)  →  Services (core/services/)  →  Repositories (core/repositories/)  →  Models (core/models/)  →  SQLite
```

- **Models** (`core/models/`): SQLAlchemy ORM — Person, Family, Event, ChildInFamily, CalendarDate, Relation, Note, Media, Source. All inherit from `alchemyBase.Base`.
- **Repositories** (`core/repositories/`): CRUD data access per model. Each follows `add_*/get_*_by_id/update_*_by_id/delete_*` pattern.
- **Services** (`core/services/`): Business logic — `CalendarConverter` (Gregorian/Julian/French Republican/Hebrew via Julian Day Number), `LanguageManager` (JSON-based i18n from `core/locales/base.json`), `ExtendedJinja2Templates`.
- **Database** (`core/database.py`): `Database` class creates SQLite in `core/bases/`. `BaseManager` handles lifecycle (create, delete, rename, cleanup/VACUUM). Base names validated with `^[A-Za-z0-9_-]{1,64}$`.

### Web Routes

**Admin (web/admin/routes/):** `/api/bases` CRUD, stats, export/import (sqlite/zip), backup/restore, merge (stub 501), create empty base.

**Public (web/server/routes/):** Homepage with base list, base detail view, calendar converter (`/calendars`, `/api/convert-date`), language switching.

### Docker

`docker/docker-compose.yml` runs both services. Volumes mount `../geneweb:/app/geneweb` for live reload. Separate Dockerfiles: `Dockerfile` (gwd) and `Dockerfile.admin` (gwsetup). Base image: Python 3.10-slim.

## Architecture — Legacy (Reference)

Flask app in `src/web/app.py`. Key differences from geneweb-python to note:

- **i18n**: 912 translation keys across 34 languages in `src/i18n/translations.py` (Python dict). Templates use `data-i18n` attributes + `<!--TRANSLATIONS-->` placeholder injected server-side as `window.TRANSLATIONS`.
- **Templates**: Full genealogy UI — `base.html` (main GeneWeb interface with search, tools, books sections), `welcome.html` (management hub: GEDCOM import/export, cleanup, rename, delete, merge), `list.html`, `cleanup.html`, `rename.html`, `delete.html`, `merge.html`, `START.htm`.
- **Frontend**: Bootstrap 4.6, jQuery 3.7, Font Awesome 6.5, DataTables, Select2.
- **Terraform** (`terraform/`): Deploys to Render free tier (Frankfurt). Uses `render-oss/render` provider v1.4. Gunicorn start command. Requires `render_api_key` and `render_owner_id` in `terraform.tfvars`.

## Key Gaps (geneweb-python vs Legacy)

- Missing comprehensive i18n (34 languages, 912 keys)
- Missing full template set (base.html genealogy UI, welcome management hub)
- Missing GEDCOM import/export
- Missing Terraform deployment config
- Merge endpoint returns 501 (not implemented)

## Tech Stack

- **Python 3.10**, FastAPI, uvicorn, SQLAlchemy, Jinja2, Pydantic
- **Database**: SQLite (file-based in `core/bases/`, in-memory for tests)
- **Testing**: pytest + pytest-mock + coverage
- **Linting**: pycodestyle (PEP8)
- **Security**: pip-audit
- **Deployment target**: Render (via Terraform with `render-oss/render` provider)

# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

SoTo is a Flask web application backed by SQLAlchemy with an SQLite database and Jinja2 HTML templates. Users create Sections that contain Goals and ShoppingItems.

## Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run the development server
python run.py

# Run tests
pytest

# Run a single test
pytest tests/test_<name>.py::test_function_name
```

The database (`soto.db`) is created automatically on first run via `db.create_all()` in `create_app()`. No migration step is needed unless Flask-Migrate is added later.

## Architecture

### App Factory (`app/__init__.py`)

`create_app(config_name)` wires up SQLAlchemy, Flask-Login, and registers all five blueprints. The `db` and `login_manager` objects live at module level here and are imported by routes and models.

### Models (`app/models.py`)

Four models with this ownership chain: `User → Section → Goal / ShoppingItem`

- Deleting a `Section` cascades to its `Goal` and `ShoppingItem` rows.
- `Goal` and `ShoppingItem` both carry a `priority` integer (1=Low, 2=Medium, 3=High) with class constants `PRIORITY_LOW/MEDIUM/HIGH` and a `priority_label` property.
- `User.set_password` / `User.check_password` wrap Werkzeug hashing — never store or compare raw passwords directly.

### Blueprints (`app/routes/`)

| Blueprint | Prefix | Responsibility |
|---|---|---|
| `auth` | `/` | register, login, logout |
| `dashboard` | `/` | home view with per-section stats |
| `sections` | `/sections` | CRUD for sections |
| `goals` | `/sections/<id>/goals` | CRUD + toggle for goals |
| `shopping` | `/sections/<id>/shopping` | CRUD + toggle for shopping items |

`goals.py` and `shopping.py` share the same ownership guard pattern: `_get_owned_section(section_id)` fetches the section and raises 403 if it doesn't belong to `current_user`. All write routes also verify the child record's `section_id` matches before mutating.

### Templates / Static

Templates live in `templates/` (sibling of `app/`), mirroring the blueprint structure:
`templates/auth/`, `templates/dashboard/`, `templates/sections/`, `templates/goals/`, `templates/shopping/`.

Static assets live in `static/` (sibling of `app/`).

### Configuration (`config.py`)

`DevelopmentConfig` (default) sets `DEBUG=True` and uses `soto.db` in the project root. Override `SECRET_KEY` and `DATABASE_URL` via environment variables for production.

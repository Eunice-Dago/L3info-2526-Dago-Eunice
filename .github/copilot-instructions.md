## Quick orientation

This repo is a small Django project (project module: `tp3`). Key application folders: `website`, `Services` (note the capitalized app directory), `blog`, `pricing`, `about`, `contact`, `gallery`.

Keep these facts in mind when working as an automated coding agent: templates live under the top-level `templates/website/pages/` directory and many apps also include app-level templates under `website/templates/website/pages/`. Static assets are under `website/static/website/assets/`.

## How to run / developer commands
- Activate the virtualenv in the repo (the project includes an `env/` venv):
  - `source env/bin/activate`
- Typical management commands (run from repo root):
  - `python3 manage.py makemigrations <AppName>` — use the exact app label as listed in `INSTALLED_APPS` (case-sensitive; e.g. `Services`).
  - `python3 manage.py migrate`
  - `python3 manage.py runserver`
  - `python3 manage.py createsuperuser`
  - `python3 manage.py collectstatic` (for static deployment)

Note: `settings.py` uses SQLite by default (db: `db.sqlite3`) but also contains `pymysql.install_as_MySQLdb()` which may be a leftover when switching DB engines. Verify `DATABASES` before changing DB code.

## Architecture & conventions (what to know)
- Project entry: `tp3/urls.py` includes the `website` app URLs at the root — most public pages are in `website/urls.py` and `website/views.py`.
- Templates:
  - Project-level templates: `/templates/website/pages/*.html` (these are included via `TEMPLATES['DIRS']`).
  - App-level templates: `website/templates/website/pages/*` (loaded because `APP_DIRS = True`).
  - When modifying a template, check both locations to avoid editing a duplicate.
- Static files are under `website/static/website/assets/` (CSS, JS, images). `STATIC_ROOT` is set to `staticfiles` in settings.
- Language / locale: `LANGUAGE_CODE = 'fr-fr'` — strings and templates may be French by convention.

## Project-specific pitfalls & examples (be explicit)
- App name case: `Services` is listed in `INSTALLED_APPS` with a capital S and the directory is `Services/`. Use that exact name when running Django management commands (e.g. `makemigrations Services`).
- Mismatched names in root urls: `tp3/urls.py` imports names like `Page`, `Section`, `PageSection`, `Menu` from `website.views`, but the actual view functions are named `list_Pages`, `list_Sections`, `list_Page_Sections`, `list_Menus` and `website/urls.py` already exposes those endpoints. Avoid editing `tp3/urls.py` unless you intend to fix these inconsistencies — they can cause import/runtime errors.
- Admin patterns: see `Services/admin.py` for typical ModelAdmin usage (list_display, list_filter, search_fields, readonly_fields). Follow the same patterns when adding admin registrations to other apps.

## When making code changes
- Before changing templates, run the server and verify which template path is used for the page (edit the one that is actually rendered). Use Django's template debug output or search for the filename across both `templates/` and app `templates/`.
- For DB changes: create migrations via `makemigrations <AppName>`; if migrations fail, confirm the correct app label and check for missing imports in `models.py`.
- Tests: there are no prominent test suites in the repository root. Use `python3 manage.py test` if you add tests.

## Helpful file references (examples you may open)
- `tp3/settings.py` — INSTALLED_APPS, TEMPLATES, DATABASES, LANGUAGE_CODE
- `tp3/urls.py` — project-level routes (note the Page/Section import mismatch)
- `website/urls.py`, `website/views.py`, `website/templates/website/pages/` — main pages and view naming patterns (e.g., `list_Pages`, `index`, `about`)
- `Services/admin.py` — how admin.ModelAdmin is configured for app models

## How to proceed as an AI coding agent
- Prefer minimal, non-breaking changes. If you must change a root routing or an INSTALLED_APPS entry, run migrations and start the server locally first.
- When you see duplicate templates, mention both paths in the PR and prefer editing the project-level `templates/` copy unless the change is app-scoped.
- If you encounter inconsistent names (like the import mismatch in `tp3/urls.py`), open an Issue and propose a minimal fix. If asked to fix automatically, update imports to reference the actual view callables or remove the duplicate route to avoid double-routing.

---
If any section should be expanded (more run commands, CI, or deployment notes), tell me what you want included and I will update this file. 

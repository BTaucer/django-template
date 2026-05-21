# Django project template

Reusable Django 6 starter for small-business API apps. Clone, rename, build.

## Stack

- Python 3.13, [uv](https://docs.astral.sh/uv/) for dependency management
- Django 6, Postgres via `psycopg`
- `django-allauth` (email login + Google OAuth)
- `django-anymail` with Postmark for transactional email
- `sentry-sdk` for production error reporting
- `argon2-cffi` as the default password hasher
- Custom `backoffice` app gated to staff users via middleware (replaces Django admin entirely)

No static-file serving baked in (no WhiteNoise). The deployment layer (reverse proxy / CDN) handles `/static/` if needed.

## Quickstart

```bash
uv sync
cp .env.example .env
# generate SECRET_KEY
python -c "import secrets; print(secrets.token_urlsafe(50))"
# paste into .env, then:
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Environments

Settings are split across `config/settings/{base,dev,prod}.py`. The module loaded is chosen by `DJANGO_ENV` in `.env`:

- `dev` — default; `DEBUG=True`, console email, debug toolbar, django-extensions.
- `prod` — `DEBUG=False`, security headers, HSTS, Postmark email, Sentry if `SENTRY_DSN` is set.

Per-developer overrides go in `.env`, not in a settings file.

## Adding a new app

Apps live under `apps/` and import via dotted paths (`apps.users`, `apps.backoffice`):

```bash
mkdir apps/<name>
python manage.py startapp <name> apps/<name>
```

Then in the generated `apps/<name>/apps.py`, change `name = "<name>"` to `name = "apps.<name>"` and add `label = "<name>"`. Finally add `"apps.<name>"` to `LOCAL_APPS` in `config/settings/base.py`.

## Backoffice

The `backoffice` app is mounted at `/backoffice/` and gated by `StaffOnlyBackofficeMiddleware`:

- Anonymous users hitting `/backoffice/*` are redirected to login.
- Authenticated users without `is_staff=True` receive 403.
- The middleware uses Django's URL resolver to detect backoffice routes via `app_name = "backoffice"`, so you can change where it's mounted in `config/urls.py` without touching middleware.

To swap the check from `is_staff` to `is_superuser` (stricter), edit `apps/backoffice/middleware.py`. Add views/URLs as you normally would — no per-view auth decorators needed.

Django's built-in admin (`django.contrib.admin`) is **not** installed. If you ever need it back, re-add `"django.contrib.admin"` to `DJANGO_APPS` in `base.py` and mount `path("admin/", admin.site.urls)` in `config/urls.py`.

## Google OAuth

Set `GOOGLE_OAUTH_CLIENT_ID` and `GOOGLE_OAUTH_CLIENT_SECRET` in `.env`. allauth reads them from `SOCIALACCOUNT_PROVIDERS["google"]["APP"]` in `base.py`, so no `SocialApp` admin entry is required.

## Postmark

1. Create a Postmark server token.
2. Set `POSTMARK_SERVER_TOKEN`, `DEFAULT_FROM_EMAIL`, `SERVER_EMAIL` in `.env`.
3. In `dev` the console backend is used (emails print to terminal); in `prod`, `anymail.backends.postmark.EmailBackend` sends through Postmark.

## Sentry

Set `SENTRY_DSN` in production `.env`. Leave empty to disable. `SENTRY_ENVIRONMENT` defaults to `production`.

## Redis cache

Optional. Set `REDIS_URL=redis://...` to use Redis; otherwise local-memory cache is used (single-process; fine for dev / small deployments).

## Lint

```bash
uv run ruff check
uv run ruff format
```

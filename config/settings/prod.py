import sentry_sdk

from .base import *  # noqa: F401,F403

DEBUG = False

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

SECURE_HSTS_SECONDS = 60 * 60 * 24 * 365
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_REFERRER_POLICY = "same-origin"
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"

EMAIL_BACKEND = "anymail.backends.postmark.EmailBackend"

_sentry_dsn = env("SENTRY_DSN", default="")  # noqa: F405
if _sentry_dsn:
    sentry_sdk.init(
        dsn=_sentry_dsn,
        environment=env("SENTRY_ENVIRONMENT", default="production"),  # noqa: F405
        send_default_pii=False,
    )

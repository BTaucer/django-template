from django.conf import settings
from django.urls import include, path

urlpatterns = [
    path("accounts/", include("allauth.urls")),
    path("backoffice/", include("apps.backoffice.urls")),
]

if settings.DEBUG:
    urlpatterns += [path("__debug__/", include("debug_toolbar.urls"))]

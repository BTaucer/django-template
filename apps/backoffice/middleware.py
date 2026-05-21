from django.contrib.auth.views import redirect_to_login
from django.http import HttpResponseForbidden
from django.urls import Resolver404, resolve


class StaffOnlyBackofficeMiddleware:
    """Gates every URL routed to the ``backoffice`` app to ``is_staff`` users.

    Anonymous → redirected to login. Authenticated non-staff → 403.
    Switch the ``is_staff`` check to ``is_superuser`` for stricter access.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            match = resolve(request.path_info)
        except Resolver404:
            return self.get_response(request)
        if match.app_name == "backoffice":
            if not request.user.is_authenticated:
                return redirect_to_login(request.get_full_path())
            if not request.user.is_staff:
                return HttpResponseForbidden("Forbidden")
        return self.get_response(request)

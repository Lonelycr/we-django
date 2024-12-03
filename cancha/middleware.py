from django.contrib.auth import logout

class LogoutOnStartMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Cerrar sesión para todos los usuarios
        if request.user.is_authenticated:
            logout(request)
        response = self.get_response(request)
        return response
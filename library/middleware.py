from django.shortcuts import redirect
from django.urls import reverse

class RegistrationRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        exempt_urls = [
            reverse('login'),
            reverse('register'),
        ]

        if not request.user.is_authenticated and request.path not in exempt_urls:
            return redirect(reverse('register'))

        return self.get_response(request)

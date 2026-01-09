import re
from django.shortcuts import redirect
from django.urls import reverse
from django.conf import settings


class LoginRequiredMiddleware:
    """
    Middleware that requires login for all views except those in EXEMPT_URLs.
    
    Provides automatic redirect to login page for unauthenticated users.
    Respects EXEMPT_URLS setting for public pages.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        self.exempt_urls = [re.compile(url) for url in getattr(settings, 'EXEMPT_URLS', [])]
    
    def __call__(self, request):
        # Check if URL is exempt
        path = request.path
        
        # Allow exempt URLs to be accessed without authentication
        for exempt_url in self.exempt_urls:
            if exempt_url.match(path):
                return self.get_response(request)
        
        # Allow admin and static/media files
        if path.startswith('/admin/') or path.startswith('/static/') or path.startswith('/media/'):
            return self.get_response(request)
        
        # Check if user is authenticated
        if not request.user.is_authenticated:
            return redirect('accounts:login')
        
        return self.get_response(request)

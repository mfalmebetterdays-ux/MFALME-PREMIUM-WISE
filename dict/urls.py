from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from django.http import HttpResponse
from myapp import views

# Simple robots.txt view
def robots_txt(request):
    lines = [
        "User-agent: *",
        "Disallow: /admin/",
        "Disallow: /admin-login/",
        "Disallow: /dashboard/",
        "Allow: /",
        "",
        "# Sitemaps",
        "Sitemap: https://tradewise.up.railway.app/sitemap.xml",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")

# Simple security.txt view (optional but recommended)
def security_txt(request):
    lines = [
        "Contact: mailto:security@tradewise-hub.com",
        "Expires: 2026-12-31T23:59:59.000Z",
        "Preferred-Languages: en",
        "Canonical: https://tradewise.up.railway.app/.well-known/security.txt",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")

urlpatterns = [
    # Static files that need to be served
    path('robots.txt', robots_txt, name='robots'),
    path('.well-known/security.txt', security_txt, name='security'),
    
    # Catch ALL old admin URLs first with redirects
    path('admin/login/', RedirectView.as_view(url='/admin-login/', permanent=True)),
    path('admin/logout/', RedirectView.as_view(url='/admin-login/', permanent=True)),
    path('admin/', RedirectView.as_view(url='/admin-login/', permanent=True)),
    
    # Include your app URLs
    path('', include('myapp.urls')),
    
    # Django admin (optional - protected by custom admin login)
    path('django-admin/', admin.site.urls),

    # Test endpoints (should be removed in production or protected)
    path('test-sendgrid-now/', views.test_sendgrid_now, name='test_sendgrid_now'),
]

# Serve media and static files in development only
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Error handlers
handler404 = 'myapp.views.handler404'
handler500 = 'myapp.views.handler500'
handler403 = 'myapp.views.handler403'  # Add this if you have a 403 handler
handler400 = 'myapp.views.handler400'  # Add this if you have a 400 handler
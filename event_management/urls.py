"""
URL configuration for event_management project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse
from django.shortcuts import redirect
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

def health_check(request):
    """Simple health check endpoint for deployment platforms."""
    return JsonResponse({
        'status': 'healthy',
        'message': 'Django Event Management System is running'
    })

def root_redirect(request):
    """Redirect root URL to API documentation."""
    return redirect('/swagger/')

# Swagger/OpenAPI documentation
schema_view = get_schema_view(
    openapi.Info(
        title="Event Management API",
        default_version='v1',
        description="API for managing events, users, and notifications",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@eventmanagement.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('', root_redirect, name='root_redirect'),
    path('admin/', admin.site.urls),
    path('api/v1/', include('events.urls')),
    path('api/v1/', include('users.urls')),
    path('api/v1/', include('notifications.urls')),
    path('health/', health_check, name='health_check'),
    
    # API Documentation
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Serve static files in production
if not settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) 
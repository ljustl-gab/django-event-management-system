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

def admin_test(request):
    """Test admin functionality."""
    try:
        from django.contrib.auth import get_user_model
        User = get_user_model()
        user_count = User.objects.count()
        return JsonResponse({
            'status': 'admin_test',
            'user_count': user_count,
            'message': 'Admin test successful'
        })
    except Exception as e:
        return JsonResponse({
            'status': 'admin_test_error',
            'error': str(e),
            'message': 'Admin test failed'
        }, status=500)

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
    path('admin-test/', admin_test, name='admin_test'),
    
    # API Documentation
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 
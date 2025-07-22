"""
URL patterns for the events app.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EventViewSet, EventParticipantViewSet

router = DefaultRouter()
router.register(r'events', EventViewSet, basename='event')
router.register(r'participants', EventParticipantViewSet, basename='participant')

urlpatterns = [
    path('', include(router.urls)),
] 
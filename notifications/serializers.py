"""
Serializers for Notification models.
"""

from rest_framework import serializers
from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    """
    Serializer for Notification model.
    """
    class Meta:
        model = Notification
        fields = [
            'id', 'notification_type', 'title', 'message',
            'is_read', 'created_at', 'read_at', 'event_id', 'event_title'
        ]
        read_only_fields = [
            'id', 'notification_type', 'title', 'message',
            'created_at', 'read_at', 'event_id', 'event_title'
        ]


class NotificationUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating notification read status.
    """
    class Meta:
        model = Notification
        fields = ['is_read'] 
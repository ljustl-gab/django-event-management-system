"""
Serializers for Event models.
"""

from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.utils import timezone
from .models import Event, EventParticipant

User = get_user_model()


class UserBasicSerializer(serializers.ModelSerializer):
    """
    Basic user serializer for event participants.
    """
    full_name = serializers.ReadOnlyField()
    
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'full_name', 'image']


class EventSerializer(serializers.ModelSerializer):
    """
    Serializer for Event model.
    """
    created_by = UserBasicSerializer(read_only=True)
    participant_count = serializers.ReadOnlyField()
    is_full = serializers.ReadOnlyField()
    is_past = serializers.ReadOnlyField()
    available_spots = serializers.ReadOnlyField()
    
    class Meta:
        model = Event
        fields = [
            'id', 'title', 'description', 'date', 'time', 'location',
            'max_participants', 'created_by', 'created_at', 'updated_at',
            'is_active', 'participant_count', 'is_full', 'is_past',
            'available_spots'
        ]
        read_only_fields = ['id', 'created_by', 'created_at', 'updated_at']


class EventCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating events.
    """
    class Meta:
        model = Event
        fields = [
            'title', 'description', 'date', 'time', 'location',
            'max_participants', 'is_active'
        ]
    
    def validate_date(self, value):
        """Validate that event date is not in the past."""
        if value < timezone.now().date():
            raise serializers.ValidationError("Event date cannot be in the past")
        return value
    
    def create(self, validated_data):
        """Create event with current user as creator."""
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)


class EventUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating events.
    """
    class Meta:
        model = Event
        fields = [
            'title', 'description', 'date', 'time', 'location',
            'max_participants', 'is_active'
        ]
    
    def validate_date(self, value):
        """Validate that event date is not in the past."""
        if value < timezone.now().date():
            raise serializers.ValidationError("Event date cannot be in the past")
        return value


class EventParticipantSerializer(serializers.ModelSerializer):
    """
    Serializer for EventParticipant model.
    """
    user = UserBasicSerializer(read_only=True)
    event = EventSerializer(read_only=True)
    
    class Meta:
        model = EventParticipant
        fields = [
            'id', 'event', 'user', 'registered_at', 'is_active'
        ]
        read_only_fields = ['id', 'registered_at']


class EventParticipantCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating event participants.
    """
    class Meta:
        model = EventParticipant
        fields = ['event']
    
    def validate_event(self, value):
        """Validate event for participation."""
        user = self.context['request'].user
        
        # Check if user is already registered
        if EventParticipant.objects.filter(event=value, user=user, is_active=True).exists():
            raise serializers.ValidationError("You are already registered for this event")
        
        # Check if event is full
        if value.is_full:
            raise serializers.ValidationError("Event is full")
        
        # Check if event is in the past
        if value.is_past:
            raise serializers.ValidationError("Cannot register for past events")
        
        return value
    
    def create(self, validated_data):
        """Create event participant with current user."""
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class EventReportSerializer(serializers.Serializer):
    """
    Serializer for event reports.
    """
    event_id = serializers.IntegerField()
    event_title = serializers.CharField()
    participant_count = serializers.IntegerField()
    participants = UserBasicSerializer(many=True)
    created_at = serializers.DateTimeField()
    date = serializers.DateField()
    time = serializers.TimeField()
    location = serializers.CharField() 
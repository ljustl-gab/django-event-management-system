"""
Admin interface for Event models.
"""

from django.contrib import admin
from .models import Event, EventParticipant


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    """
    Admin interface for Event model.
    """
    list_display = [
        'title', 'date', 'time', 'location', 'created_by',
        'participant_count', 'is_active', 'created_at'
    ]
    list_filter = ['date', 'is_active', 'created_at']
    search_fields = ['title', 'description', 'location', 'created_by__email']
    ordering = ['-date', '-time']
    readonly_fields = ['created_at', 'updated_at', 'participant_count']
    
    fieldsets = (
        ('Event Information', {
            'fields': ('title', 'description', 'date', 'time', 'location')
        }),
        ('Capacity', {
            'fields': ('max_participants',)
        }),
        ('Status', {
            'fields': ('is_active', 'created_by')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def participant_count(self, obj):
        """Display participant count."""
        return obj.participant_count
    participant_count.short_description = 'Participants'


@admin.register(EventParticipant)
class EventParticipantAdmin(admin.ModelAdmin):
    """
    Admin interface for EventParticipant model.
    """
    list_display = [
        'user', 'event', 'registered_at', 'is_active'
    ]
    list_filter = ['is_active', 'registered_at', 'event__date']
    search_fields = [
        'user__email', 'user__first_name', 'user__last_name',
        'event__title'
    ]
    ordering = ['-registered_at']
    readonly_fields = ['registered_at']
    
    fieldsets = (
        ('Participant Information', {
            'fields': ('user', 'event')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Registration', {
            'fields': ('registered_at',),
            'classes': ('collapse',)
        }),
    ) 
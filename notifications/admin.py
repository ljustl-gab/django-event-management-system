"""
Admin interface for Notification model.
"""

from django.contrib import admin
from .models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    """
    Admin interface for Notification model.
    """
    list_display = [
        'user', 'notification_type', 'title', 'is_read', 'created_at'
    ]
    list_filter = ['notification_type', 'is_read', 'created_at']
    search_fields = [
        'user__email', 'user__first_name', 'user__last_name',
        'title', 'message', 'event_title'
    ]
    ordering = ['-created_at']
    readonly_fields = ['created_at', 'read_at']
    
    fieldsets = (
        ('Notification Information', {
            'fields': ('user', 'notification_type', 'title', 'message')
        }),
        ('Event Information', {
            'fields': ('event_id', 'event_title'),
            'classes': ('collapse',)
        }),
        ('Status', {
            'fields': ('is_read',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'read_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['mark_as_read', 'mark_as_unread']
    
    def mark_as_read(self, request, queryset):
        """Mark selected notifications as read."""
        count = queryset.update(is_read=True)
        self.message_user(request, f'{count} notifications marked as read.')
    mark_as_read.short_description = "Mark selected notifications as read"
    
    def mark_as_unread(self, request, queryset):
        """Mark selected notifications as unread."""
        count = queryset.update(is_read=False, read_at=None)
        self.message_user(request, f'{count} notifications marked as unread.')
    mark_as_unread.short_description = "Mark selected notifications as unread" 
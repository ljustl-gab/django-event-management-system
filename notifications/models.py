"""
Notification models for the event management system.
"""

from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class Notification(models.Model):
    """
    Model for storing user notifications.
    """
    NOTIFICATION_TYPES = [
        ('event_update', _('Event Update')),
        ('event_cancellation', _('Event Cancellation')),
        ('registration_confirmation', _('Registration Confirmation')),
        ('reminder', _('Event Reminder')),
    ]
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='notifications',
        verbose_name=_('user')
    )
    notification_type = models.CharField(
        _('notification type'),
        max_length=50,
        choices=NOTIFICATION_TYPES
    )
    title = models.CharField(_('title'), max_length=200)
    message = models.TextField(_('message'))
    is_read = models.BooleanField(_('is read'), default=False)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    read_at = models.DateTimeField(_('read at'), null=True, blank=True)
    
    # Optional fields for event-related notifications
    event_id = models.PositiveIntegerField(
        _('event id'),
        null=True,
        blank=True
    )
    event_title = models.CharField(
        _('event title'),
        max_length=200,
        null=True,
        blank=True
    )
    
    class Meta:
        verbose_name = _('notification')
        verbose_name_plural = _('notifications')
        db_table = 'notifications'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'is_read']),
            models.Index(fields=['notification_type']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"{self.user.email} - {self.title}"
    
    def mark_as_read(self):
        """Mark notification as read."""
        if not self.is_read:
            self.is_read = True
            from django.utils import timezone
            self.read_at = timezone.now()
            self.save() 
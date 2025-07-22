"""
Event models for the event management system.
"""

from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator
from django.utils import timezone

User = get_user_model()


class Event(models.Model):
    """
    Event model for managing conferences and seminars.
    """
    title = models.CharField(_('title'), max_length=200)
    description = models.TextField(_('description'))
    date = models.DateField(_('date'))
    time = models.TimeField(_('time'))
    location = models.CharField(_('location'), max_length=500)
    max_participants = models.PositiveIntegerField(
        _('maximum participants'),
        null=True,
        blank=True,
        help_text=_('Leave empty for unlimited participants')
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='created_events',
        verbose_name=_('created by')
    )
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    is_active = models.BooleanField(_('is active'), default=True)
    
    class Meta:
        verbose_name = _('event')
        verbose_name_plural = _('events')
        db_table = 'events'
        ordering = ['-date', '-time']
        indexes = [
            models.Index(fields=['date', 'time']),
            models.Index(fields=['created_by']),
            models.Index(fields=['is_active']),
        ]
    
    def __str__(self):
        return f"{self.title} - {self.date} {self.time}"
    
    @property
    def participant_count(self):
        """Return the number of participants registered for this event."""
        return self.participants.filter(is_active=True).count()
    
    @property
    def is_full(self):
        """Check if the event is full."""
        if self.max_participants is None:
            return False
        return self.participant_count >= self.max_participants
    
    @property
    def is_past(self):
        """Check if the event is in the past."""
        event_datetime = timezone.make_aware(
            timezone.datetime.combine(self.date, self.time)
        )
        return event_datetime < timezone.now()
    
    @property
    def available_spots(self):
        """Return the number of available spots."""
        if self.max_participants is None:
            return None
        return max(0, self.max_participants - self.participant_count)


class EventParticipant(models.Model):
    """
    Model to track participants for events.
    """
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name='participants',
        verbose_name=_('event')
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='event_participations',
        verbose_name=_('user')
    )
    registered_at = models.DateTimeField(_('registered at'), auto_now_add=True)
    is_active = models.BooleanField(_('is active'), default=True)
    
    class Meta:
        verbose_name = _('event participant')
        verbose_name_plural = _('event participants')
        db_table = 'event_participants'
        unique_together = ['event', 'user']
        ordering = ['-registered_at']
        indexes = [
            models.Index(fields=['event', 'user']),
            models.Index(fields=['registered_at']),
            models.Index(fields=['is_active']),
        ]
    
    def __str__(self):
        return f"{self.user.full_name} - {self.event.title}"
    
    def save(self, *args, **kwargs):
        """Override save to check event capacity."""
        if not self.pk:  # Only on creation
            if self.event.is_full:
                raise ValueError("Event is full")
        super().save(*args, **kwargs) 
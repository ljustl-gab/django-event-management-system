"""
Celery tasks for notification processing.
"""

import logging
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from django.template.loader import render_to_string

from .models import Notification
from events.models import Event, EventParticipant

logger = logging.getLogger(__name__)


@shared_task
def send_registration_confirmation(participant_id):
    """
    Send registration confirmation email to participant.
    """
    try:
        participant = EventParticipant.objects.select_related('user', 'event').get(id=participant_id)
        
        # Create notification
        Notification.objects.create(
            user=participant.user,
            notification_type='registration_confirmation',
            title='Registration Confirmed',
            message=f'Your registration for "{participant.event.title}" has been confirmed.',
            event_id=participant.event.id,
            event_title=participant.event.title
        )
        
        # Send email
        subject = f'Registration Confirmed - {participant.event.title}'
        message = f"""
        Hello {participant.user.first_name},
        
        Your registration for "{participant.event.title}" has been confirmed.
        
        Event Details:
        - Date: {participant.event.date}
        - Time: {participant.event.time}
        - Location: {participant.event.location}
        
        We look forward to seeing you!
        """
        
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[participant.user.email],
            fail_silently=True
        )
        
        logger.info(f'Registration confirmation sent to {participant.user.email}')
        
    except EventParticipant.DoesNotExist:
        logger.error(f'Participant with id {participant_id} not found')
    except Exception as e:
        logger.error(f'Error sending registration confirmation: {str(e)}')


@shared_task
def send_event_cancellation_notification(event_id):
    """
    Send event cancellation notification to all participants.
    """
    try:
        event = Event.objects.get(id=event_id)
        participants = EventParticipant.objects.filter(
            event=event,
            is_active=True
        ).select_related('user')
        
        for participant in participants:
            # Create notification
            Notification.objects.create(
                user=participant.user,
                notification_type='event_cancellation',
                title='Event Cancelled',
                message=f'The event "{event.title}" has been cancelled.',
                event_id=event.id,
                event_title=event.title
            )
            
            # Send email
            subject = f'Event Cancelled - {event.title}'
            message = f"""
            Hello {participant.user.first_name},
            
            We regret to inform you that the event "{event.title}" has been cancelled.
            
            We apologize for any inconvenience this may cause.
            """
            
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[participant.user.email],
                fail_silently=True
            )
        
        logger.info(f'Cancellation notifications sent to {participants.count()} participants')
        
    except Event.DoesNotExist:
        logger.error(f'Event with id {event_id} not found')
    except Exception as e:
        logger.error(f'Error sending cancellation notifications: {str(e)}')


@shared_task
def send_event_update_notification(event_id, update_message):
    """
    Send event update notification to all participants.
    """
    try:
        event = Event.objects.get(id=event_id)
        participants = EventParticipant.objects.filter(
            event=event,
            is_active=True
        ).select_related('user')
        
        for participant in participants:
            # Create notification
            Notification.objects.create(
                user=participant.user,
                notification_type='event_update',
                title='Event Updated',
                message=f'Update for "{event.title}": {update_message}',
                event_id=event.id,
                event_title=event.title
            )
            
            # Send email
            subject = f'Event Update - {event.title}'
            message = f"""
            Hello {participant.user.first_name},
            
            There has been an update to the event "{event.title}":
            
            {update_message}
            
            Event Details:
            - Date: {event.date}
            - Time: {event.time}
            - Location: {event.location}
            """
            
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[participant.user.email],
                fail_silently=True
            )
        
        logger.info(f'Update notifications sent to {participants.count()} participants')
        
    except Event.DoesNotExist:
        logger.error(f'Event with id {event_id} not found')
    except Exception as e:
        logger.error(f'Error sending update notifications: {str(e)}')


@shared_task
def send_event_reminders():
    """
    Send reminders for events happening tomorrow.
    """
    try:
        tomorrow = timezone.now().date() + timezone.timedelta(days=1)
        events = Event.objects.filter(
            date=tomorrow,
            is_active=True
        )
        
        for event in events:
            participants = EventParticipant.objects.filter(
                event=event,
                is_active=True
            ).select_related('user')
            
            for participant in participants:
                # Create notification
                Notification.objects.create(
                    user=participant.user,
                    notification_type='reminder',
                    title='Event Reminder',
                    message=f'Reminder: "{event.title}" is tomorrow!',
                    event_id=event.id,
                    event_title=event.title
                )
                
                # Send email
                subject = f'Event Reminder - {event.title}'
                message = f"""
                Hello {participant.user.first_name},
                
                This is a reminder that "{event.title}" is tomorrow!
                
                Event Details:
                - Date: {event.date}
                - Time: {event.time}
                - Location: {event.location}
                
                We look forward to seeing you!
                """
                
                send_mail(
                    subject=subject,
                    message=message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[participant.user.email],
                    fail_silently=True
                )
        
        logger.info(f'Reminders sent for {events.count()} events')
        
    except Exception as e:
        logger.error(f'Error sending event reminders: {str(e)}')


@shared_task
def cleanup_old_notifications():
    """
    Clean up notifications older than 30 days.
    """
    try:
        cutoff_date = timezone.now() - timezone.timedelta(days=30)
        deleted_count, _ = Notification.objects.filter(
            created_at__lt=cutoff_date,
            is_read=True
        ).delete()
        
        logger.info(f'Cleaned up {deleted_count} old notifications')
        
    except Exception as e:
        logger.error(f'Error cleaning up old notifications: {str(e)}') 
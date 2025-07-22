"""
Tests for Notification functionality.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.utils import timezone

from notifications.models import Notification
from events.models import Event

User = get_user_model()


class NotificationModelTest(TestCase):
    """Test cases for Notification model."""
    
    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            first_name='Test',
            last_name='User',
            password='testpass123'
        )
        
        self.notification_data = {
            'user': self.user,
            'notification_type': 'event_update',
            'title': 'Test Notification',
            'message': 'This is a test notification message.',
            'event_id': 1,
            'event_title': 'Test Event'
        }
    
    def test_create_notification(self):
        """Test creating a new notification."""
        notification = Notification.objects.create(**self.notification_data)
        self.assertEqual(notification.user, self.user)
        self.assertEqual(notification.notification_type, 'event_update')
        self.assertEqual(notification.title, 'Test Notification')
        self.assertEqual(notification.message, 'This is a test notification message.')
        self.assertFalse(notification.is_read)
        self.assertIsNone(notification.read_at)
    
    def test_notification_str_representation(self):
        """Test notification string representation."""
        notification = Notification.objects.create(**self.notification_data)
        expected_str = f"{self.user.email} - {self.notification_data['title']}"
        self.assertEqual(str(notification), expected_str)
    
    def test_mark_notification_as_read(self):
        """Test marking notification as read."""
        notification = Notification.objects.create(**self.notification_data)
        self.assertFalse(notification.is_read)
        self.assertIsNone(notification.read_at)
        
        notification.mark_as_read()
        notification.refresh_from_db()
        
        self.assertTrue(notification.is_read)
        self.assertIsNotNone(notification.read_at)
    
    def test_mark_already_read_notification(self):
        """Test marking already read notification as read."""
        notification = Notification.objects.create(**self.notification_data)
        notification.mark_as_read()
        original_read_at = notification.read_at
        
        notification.mark_as_read()
        notification.refresh_from_db()
        
        self.assertEqual(notification.read_at, original_read_at)


class NotificationAPITest(TestCase):
    """Test cases for Notification API endpoints."""
    
    def setUp(self):
        """Set up test data."""
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            first_name='Test',
            last_name='User',
            password='testpass123'
        )
        
        self.notification = Notification.objects.create(
            user=self.user,
            notification_type='event_update',
            title='Test Notification',
            message='This is a test notification message.',
            event_id=1,
            event_title='Test Event'
        )
    
    def test_list_notifications_authenticated(self):
        """Test listing notifications when authenticated."""
        self.client.force_authenticate(user=self.user)
        url = reverse('notification-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], self.notification.title)
    
    def test_list_notifications_unauthenticated(self):
        """Test listing notifications when not authenticated."""
        url = reverse('notification-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_get_notification_detail(self):
        """Test getting notification details."""
        self.client.force_authenticate(user=self.user)
        url = reverse('notification-detail', kwargs={'pk': self.notification.pk})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.notification.title)
        self.assertEqual(response.data['message'], self.notification.message)
    
    def test_get_other_user_notification(self):
        """Test getting another user's notification (should fail)."""
        other_user = User.objects.create_user(
            username='otheruser',
            email='other@example.com',
            first_name='Other',
            last_name='User',
            password='otherpass123'
        )
        
        self.client.force_authenticate(user=other_user)
        url = reverse('notification-detail', kwargs={'pk': self.notification.pk})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_mark_notification_as_read(self):
        """Test marking notification as read."""
        self.client.force_authenticate(user=self.user)
        url = reverse('notification-mark-as-read', kwargs={'pk': self.notification.pk})
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.notification.refresh_from_db()
        self.assertTrue(self.notification.is_read)
        self.assertIsNotNone(self.notification.read_at)
    
    def test_mark_all_notifications_as_read(self):
        """Test marking all notifications as read."""
        # Create additional notifications
        Notification.objects.create(
            user=self.user,
            notification_type='event_cancellation',
            title='Another Notification',
            message='Another test message.',
            is_read=False
        )
        
        self.client.force_authenticate(user=self.user)
        url = reverse('notification-mark-all-as-read')
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)
        
        # Check that all notifications are marked as read
        unread_count = Notification.objects.filter(user=self.user, is_read=False).count()
        self.assertEqual(unread_count, 0)
    
    def test_get_unread_count(self):
        """Test getting unread notification count."""
        # Create additional unread notification
        Notification.objects.create(
            user=self.user,
            notification_type='reminder',
            title='Unread Notification',
            message='Unread message.',
            is_read=False
        )
        
        self.client.force_authenticate(user=self.user)
        url = reverse('notification-unread-count')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['unread_count'], 2)  # Original + new one
    
    def test_get_recent_notifications(self):
        """Test getting recent notifications."""
        # Create additional notifications
        for i in range(15):
            Notification.objects.create(
                user=self.user,
                notification_type='event_update',
                title=f'Notification {i}',
                message=f'Message {i}',
                is_read=False
            )
        
        self.client.force_authenticate(user=self.user)
        url = reverse('notification-recent')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 10)  # Should return only 10 most recent
    
    def test_update_notification_read_status(self):
        """Test updating notification read status."""
        self.client.force_authenticate(user=self.user)
        url = reverse('notification-detail', kwargs={'pk': self.notification.pk})
        update_data = {'is_read': True}
        response = self.client.patch(url, update_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.notification.refresh_from_db()
        self.assertTrue(self.notification.is_read)
        self.assertIsNotNone(self.notification.read_at)
    
    def test_filter_notifications_by_type(self):
        """Test filtering notifications by type."""
        # Create notifications of different types
        Notification.objects.create(
            user=self.user,
            notification_type='event_cancellation',
            title='Cancellation Notification',
            message='Event cancelled.',
            is_read=False
        )
        
        self.client.force_authenticate(user=self.user)
        url = reverse('notification-list')
        response = self.client.get(url, {'notification_type': 'event_update'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['notification_type'], 'event_update')
    
    def test_filter_notifications_by_read_status(self):
        """Test filtering notifications by read status."""
        # Mark original notification as read
        self.notification.mark_as_read()
        
        # Create unread notification
        Notification.objects.create(
            user=self.user,
            notification_type='reminder',
            title='Unread Notification',
            message='Unread message.',
            is_read=False
        )
        
        self.client.force_authenticate(user=self.user)
        url = reverse('notification-list')
        response = self.client.get(url, {'is_read': 'false'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertFalse(response.data['results'][0]['is_read'])


class NotificationTaskTest(TestCase):
    """Test cases for notification tasks."""
    
    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            first_name='Test',
            last_name='User',
            password='testpass123'
        )
        
        self.event = Event.objects.create(
            title='Test Event',
            description='A test event description',
            date=timezone.now().date() + timezone.timedelta(days=7),
            time=timezone.now().time(),
            location='Test Location',
            created_by=self.user
        )
    
    def test_send_registration_confirmation_task(self):
        """Test registration confirmation task."""
        from notifications.tasks import send_registration_confirmation
        
        # Create a participant
        from events.models import EventParticipant
        participant = EventParticipant.objects.create(
            event=self.event,
            user=self.user
        )
        
        # Run the task
        result = send_registration_confirmation(participant.id)
        
        # Check that notification was created
        notification = Notification.objects.filter(
            user=self.user,
            notification_type='registration_confirmation'
        ).first()
        
        self.assertIsNotNone(notification)
        self.assertEqual(notification.title, 'Registration Confirmed')
        self.assertIn(self.event.title, notification.message)
    
    def test_send_event_cancellation_notification_task(self):
        """Test event cancellation notification task."""
        from notifications.tasks import send_event_cancellation_notification
        
        # Create participants
        from events.models import EventParticipant
        EventParticipant.objects.create(event=self.event, user=self.user)
        
        # Run the task
        result = send_event_cancellation_notification(self.event.id)
        
        # Check that notification was created
        notification = Notification.objects.filter(
            user=self.user,
            notification_type='event_cancellation'
        ).first()
        
        self.assertIsNotNone(notification)
        self.assertEqual(notification.title, 'Event Cancelled')
        self.assertIn(self.event.title, notification.message)
    
    def test_send_event_update_notification_task(self):
        """Test event update notification task."""
        from notifications.tasks import send_event_update_notification
        
        # Create participants
        from events.models import EventParticipant
        EventParticipant.objects.create(event=self.event, user=self.user)
        
        # Run the task
        update_message = "Event time has been changed to 3:00 PM"
        result = send_event_update_notification(self.event.id, update_message)
        
        # Check that notification was created
        notification = Notification.objects.filter(
            user=self.user,
            notification_type='event_update'
        ).first()
        
        self.assertIsNotNone(notification)
        self.assertEqual(notification.title, 'Event Updated')
        self.assertIn(update_message, notification.message) 
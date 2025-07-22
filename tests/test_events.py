"""
Tests for Event functionality.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.utils import timezone
from datetime import date, time, timedelta

from events.models import Event, EventParticipant

User = get_user_model()


class EventModelTest(TestCase):
    """Test cases for Event model."""
    
    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            first_name='Test',
            last_name='User',
            password='testpass123'
        )
        
        self.event_data = {
            'title': 'Test Event',
            'description': 'A test event description',
            'date': date.today() + timedelta(days=7),
            'time': time(14, 0),
            'location': 'Test Location',
            'max_participants': 50,
            'created_by': self.user
        }
    
    def test_create_event(self):
        """Test creating a new event."""
        event = Event.objects.create(**self.event_data)
        self.assertEqual(event.title, self.event_data['title'])
        self.assertEqual(event.description, self.event_data['description'])
        self.assertEqual(event.date, self.event_data['date'])
        self.assertEqual(event.time, self.event_data['time'])
        self.assertEqual(event.location, self.event_data['location'])
        self.assertEqual(event.max_participants, self.event_data['max_participants'])
        self.assertEqual(event.created_by, self.user)
    
    def test_event_str_representation(self):
        """Test event string representation."""
        event = Event.objects.create(**self.event_data)
        expected_str = f"{self.event_data['title']} - {self.event_data['date']} {self.event_data['time']}"
        self.assertEqual(str(event), expected_str)
    
    def test_event_participant_count(self):
        """Test event participant count property."""
        event = Event.objects.create(**self.event_data)
        self.assertEqual(event.participant_count, 0)
        
        # Add participants
        participant1 = User.objects.create_user(
            username='participant1',
            email='participant1@example.com',
            first_name='Participant',
            last_name='One',
            password='pass123'
        )
        participant2 = User.objects.create_user(
            username='participant2',
            email='participant2@example.com',
            first_name='Participant',
            last_name='Two',
            password='pass123'
        )
        
        EventParticipant.objects.create(event=event, user=participant1)
        EventParticipant.objects.create(event=event, user=participant2)
        
        self.assertEqual(event.participant_count, 2)
    
    def test_event_is_full(self):
        """Test event is_full property."""
        event = Event.objects.create(**self.event_data)
        self.assertFalse(event.is_full)
        
        # Add participants up to capacity
        for i in range(50):
            participant = User.objects.create_user(
                username=f'participant{i}',
                email=f'participant{i}@example.com',
                first_name=f'Participant{i}',
                last_name='User',
                password='pass123'
            )
            EventParticipant.objects.create(event=event, user=participant)
        
        self.assertTrue(event.is_full)
    
    def test_event_available_spots(self):
        """Test event available_spots property."""
        event = Event.objects.create(**self.event_data)
        self.assertEqual(event.available_spots, 50)
        
        # Add some participants
        participant = User.objects.create_user(
            username='participant',
            email='participant@example.com',
            first_name='Participant',
            last_name='User',
            password='pass123'
        )
        EventParticipant.objects.create(event=event, user=participant)
        
        self.assertEqual(event.available_spots, 49)
    
    def test_event_is_past(self):
        """Test event is_past property."""
        # Future event
        future_event = Event.objects.create(**self.event_data)
        self.assertFalse(future_event.is_past)
        
        # Past event
        past_event_data = self.event_data.copy()
        past_event_data['date'] = date.today() - timedelta(days=1)
        past_event = Event.objects.create(**past_event_data)
        self.assertTrue(past_event.is_past)


class EventAPITest(TestCase):
    """Test cases for Event API endpoints."""
    
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
        
        self.event_data = {
            'title': 'Test Event',
            'description': 'A test event description',
            'date': (date.today() + timedelta(days=7)).isoformat(),
            'time': '14:00:00',
            'location': 'Test Location',
            'max_participants': 50,
            'is_active': True
        }
    
    def test_create_event_success(self):
        """Test successful event creation."""
        self.client.force_authenticate(user=self.user)
        url = reverse('event-list')
        response = self.client.post(url, self.event_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Event.objects.count(), 1)
        
        event = Event.objects.first()
        self.assertEqual(event.title, self.event_data['title'])
        self.assertEqual(event.created_by, self.user)
    
    def test_create_event_unauthenticated(self):
        """Test event creation without authentication."""
        url = reverse('event-list')
        response = self.client.post(url, self.event_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_create_event_past_date(self):
        """Test event creation with past date."""
        self.client.force_authenticate(user=self.user)
        self.event_data['date'] = (date.today() - timedelta(days=1)).isoformat()
        url = reverse('event-list')
        response = self.client.post(url, self.event_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('date', response.data)
    
    def test_list_events(self):
        """Test listing events."""
        event = Event.objects.create(
            title='Test Event',
            description='A test event description',
            date=date.today() + timedelta(days=7),
            time=time(14, 0),
            location='Test Location',
            created_by=self.user
        )
        
        url = reverse('event-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], event.title)
    
    def test_get_event_detail(self):
        """Test getting event details."""
        event = Event.objects.create(
            title='Test Event',
            description='A test event description',
            date=date.today() + timedelta(days=7),
            time=time(14, 0),
            location='Test Location',
            created_by=self.user
        )
        
        url = reverse('event-detail', kwargs={'pk': event.pk})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], event.title)
        self.assertEqual(response.data['description'], event.description)
    
    def test_update_event_success(self):
        """Test successful event update."""
        event = Event.objects.create(
            title='Test Event',
            description='A test event description',
            date=date.today() + timedelta(days=7),
            time=time(14, 0),
            location='Test Location',
            created_by=self.user
        )
        
        self.client.force_authenticate(user=self.user)
        url = reverse('event-detail', kwargs={'pk': event.pk})
        update_data = {
            'title': 'Updated Event Title',
            'description': 'Updated description'
        }
        response = self.client.patch(url, update_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        event.refresh_from_db()
        self.assertEqual(event.title, 'Updated Event Title')
    
    def test_update_event_unauthorized(self):
        """Test event update by non-owner."""
        other_user = User.objects.create_user(
            username='otheruser',
            email='other@example.com',
            first_name='Other',
            last_name='User',
            password='otherpass123'
        )
        
        event = Event.objects.create(
            title='Test Event',
            description='A test event description',
            date=date.today() + timedelta(days=7),
            time=time(14, 0),
            location='Test Location',
            created_by=self.user
        )
        
        self.client.force_authenticate(user=other_user)
        url = reverse('event-detail', kwargs={'pk': event.pk})
        update_data = {'title': 'Unauthorized Update'}
        response = self.client.patch(url, update_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_delete_event_success(self):
        """Test successful event deletion."""
        event = Event.objects.create(
            title='Test Event',
            description='A test event description',
            date=date.today() + timedelta(days=7),
            time=time(14, 0),
            location='Test Location',
            created_by=self.user
        )
        
        self.client.force_authenticate(user=self.user)
        url = reverse('event-detail', kwargs={'pk': event.pk})
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Event.objects.filter(id=event.id).exists())
    
    def test_delete_event_unauthorized(self):
        """Test event deletion by non-owner."""
        other_user = User.objects.create_user(
            username='otheruser',
            email='other@example.com',
            first_name='Other',
            last_name='User',
            password='otherpass123'
        )
        
        event = Event.objects.create(
            title='Test Event',
            description='A test event description',
            date=date.today() + timedelta(days=7),
            time=time(14, 0),
            location='Test Location',
            created_by=self.user
        )
        
        self.client.force_authenticate(user=other_user)
        url = reverse('event-detail', kwargs={'pk': event.pk})
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Event.objects.filter(id=event.id).exists())


class EventParticipantTest(TestCase):
    """Test cases for Event Participant functionality."""
    
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
        
        self.event = Event.objects.create(
            title='Test Event',
            description='A test event description',
            date=date.today() + timedelta(days=7),
            time=time(14, 0),
            location='Test Location',
            max_participants=2,
            created_by=self.user
        )
    
    def test_register_for_event_success(self):
        """Test successful event registration."""
        self.client.force_authenticate(user=self.user)
        url = reverse('event-register', kwargs={'pk': self.event.pk})
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(EventParticipant.objects.filter(
            event=self.event,
            user=self.user,
            is_active=True
        ).exists())
    
    def test_register_for_event_unauthenticated(self):
        """Test event registration without authentication."""
        url = reverse('event-register', kwargs={'pk': self.event.pk})
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_register_for_full_event(self):
        """Test registration for a full event."""
        # Fill the event
        participant1 = User.objects.create_user(
            username='participant1',
            email='participant1@example.com',
            first_name='Participant',
            last_name='One',
            password='pass123'
        )
        participant2 = User.objects.create_user(
            username='participant2',
            email='participant2@example.com',
            first_name='Participant',
            last_name='Two',
            password='pass123'
        )
        
        EventParticipant.objects.create(event=self.event, user=participant1)
        EventParticipant.objects.create(event=self.event, user=participant2)
        
        self.client.force_authenticate(user=self.user)
        url = reverse('event-register', kwargs={'pk': self.event.pk})
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('event', response.data)
    
    def test_register_for_past_event(self):
        """Test registration for a past event."""
        past_event = Event.objects.create(
            title='Past Event',
            description='A past event',
            date=date.today() - timedelta(days=1),
            time=time(14, 0),
            location='Past Location',
            created_by=self.user
        )
        
        self.client.force_authenticate(user=self.user)
        url = reverse('event-register', kwargs={'pk': past_event.pk})
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('event', response.data)
    
    def test_unregister_from_event_success(self):
        """Test successful event unregistration."""
        EventParticipant.objects.create(event=self.event, user=self.user)
        
        self.client.force_authenticate(user=self.user)
        url = reverse('event-unregister', kwargs={'pk': self.event.pk})
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        participant = EventParticipant.objects.get(event=self.event, user=self.user)
        self.assertFalse(participant.is_active)
    
    def test_unregister_from_event_not_registered(self):
        """Test unregistration when not registered."""
        self.client.force_authenticate(user=self.user)
        url = reverse('event-unregister', kwargs={'pk': self.event.pk})
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
    
    def test_get_event_participants(self):
        """Test getting event participants."""
        participant = User.objects.create_user(
            username='participant',
            email='participant@example.com',
            first_name='Participant',
            last_name='User',
            password='pass123'
        )
        EventParticipant.objects.create(event=self.event, user=participant)
        
        url = reverse('event-participants', kwargs={'pk': self.event.pk})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['user']['email'], participant.email)
    
    def test_get_event_report(self):
        """Test getting event report."""
        participant = User.objects.create_user(
            username='participant',
            email='participant@example.com',
            first_name='Participant',
            last_name='User',
            password='pass123'
        )
        EventParticipant.objects.create(event=self.event, user=participant)
        
        url = reverse('event-report', kwargs={'pk': self.event.pk})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['event_title'], self.event.title)
        self.assertEqual(response.data['participant_count'], 1)
        self.assertEqual(len(response.data['participants']), 1) 
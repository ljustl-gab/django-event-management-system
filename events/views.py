"""
Views for Event management.
"""

from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Prefetch
from django.utils import timezone

from .models import Event, EventParticipant
from .serializers import (
    EventSerializer,
    EventCreateSerializer,
    EventUpdateSerializer,
    EventParticipantSerializer,
    EventParticipantCreateSerializer,
    EventReportSerializer
)


class EventViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Event CRUD operations.
    """
    queryset = Event.objects.select_related('created_by').prefetch_related(
        Prefetch('participants', queryset=EventParticipant.objects.filter(is_active=True))
    )
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['date', 'is_active', 'created_by']
    search_fields = ['title', 'description', 'location']
    ordering_fields = ['date', 'time', 'created_at', 'title']
    ordering = ['-date', '-time']
    
    def get_serializer_class(self):
        """Return appropriate serializer class based on action."""
        if self.action == 'create':
            return EventCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return EventUpdateSerializer
        return EventSerializer
    
    def get_queryset(self):
        """Return queryset based on user permissions."""
        queryset = super().get_queryset()
        
        # Filter by date range if provided
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        
        if start_date:
            queryset = queryset.filter(date__gte=start_date)
        if end_date:
            queryset = queryset.filter(date__lte=end_date)
        
        return queryset
    
    @action(detail=True, methods=['post'])
    def register(self, request, pk=None):
        """Register current user for an event."""
        event = self.get_object()
        serializer = EventParticipantCreateSerializer(
            data={'event': event.id},
            context={'request': request}
        )
        
        if serializer.is_valid():
            participant = serializer.save()
            # Trigger async task for confirmation email
            try:
                from notifications.tasks import send_registration_confirmation
                send_registration_confirmation.delay(participant.id)
            except ImportError:
                # Handle case where notifications app is not available
                pass
            
            return Response(
                {'message': 'Successfully registered for event'},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def unregister(self, request, pk=None):
        """Unregister current user from an event."""
        event = self.get_object()
        try:
            participant = EventParticipant.objects.get(
                event=event,
                user=request.user,
                is_active=True
            )
            participant.is_active = False
            participant.save()
            return Response({'message': 'Successfully unregistered from event'})
        except EventParticipant.DoesNotExist:
            return Response(
                {'error': 'You are not registered for this event'},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=True, methods=['get'])
    def participants(self, request, pk=None):
        """Get list of participants for an event."""
        event = self.get_object()
        participants = EventParticipant.objects.filter(
            event=event,
            is_active=True
        ).select_related('user')
        
        serializer = EventParticipantSerializer(participants, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def report(self, request, pk=None):
        """Generate report for an event."""
        event = self.get_object()
        
        # Get active participants with user details
        participants = event.participants.filter(is_active=True).select_related('user')
        participant_users = [p.user for p in participants]
        
        report_data = {
            'event_id': event.id,
            'event_title': event.title,
            'participant_count': len(participant_users),
            'participants': participant_users,
            'created_at': event.created_at,
            'date': event.date,
            'time': event.time,
            'location': event.location,
        }
        
        serializer = EventReportSerializer(report_data)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def my_events(self, request):
        """Get events created by current user."""
        events = self.get_queryset().filter(created_by=request.user)
        page = self.paginate_queryset(events)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(events, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def registered_events(self, request):
        """Get events where current user is registered."""
        user_participations = EventParticipant.objects.filter(
            user=request.user,
            is_active=True
        ).select_related('event', 'event__created_by')
        
        events = [p.event for p in user_participations]
        page = self.paginate_queryset(events)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(events, many=True)
        return Response(serializer.data)
    
    def destroy(self, request, *args, **kwargs):
        """Delete event with permission check."""
        event = self.get_object()
        if event.created_by != request.user and not request.user.is_staff:
            return Response(
                {'error': 'You can only delete events you created'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Notify participants about event cancellation
        try:
            from notifications.tasks import send_event_cancellation_notification
            send_event_cancellation_notification.delay(event.id)
        except ImportError:
            # Handle case where notifications app is not available
            pass
        
        return super().destroy(request, *args, **kwargs)


class EventParticipantViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for EventParticipant read operations.
    """
    queryset = EventParticipant.objects.select_related('user', 'event')
    serializer_class = EventParticipantSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['event', 'user', 'is_active']
    ordering_fields = ['registered_at']
    ordering = ['-registered_at']
    
    def get_queryset(self):
        """Return queryset based on user permissions."""
        queryset = super().get_queryset()
        
        # Staff can see all participants, users can only see their own
        if not self.request.user.is_staff:
            queryset = queryset.filter(user=self.request.user)
        
        return queryset 
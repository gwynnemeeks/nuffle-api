"""View module for handling requests about players"""

from django.contrib.auth import get_user_model
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from nuffleapi.models import Coach, Event, Team

class Events(ViewSet):
    """Level up events"""

    def retrieve(self, request, pk=None):
        """Handle GET requests for single event

        Returns:
            Response -- JSON serialized event
        """
        try:
            event = Event.objects.get(pk=pk)
            serializer = EventSerializer(event, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """Handle GET requests to get all events

        Returns:
            Response -- JSON serialized list of events
        """
        events = Event.objects.all()

        # Note the addtional `many=True` argument to the
        # serializer. It's needed when you are serializing
        # a list of objects instead of a single object.
        serializer = EventSerializer(
            events, many=True, context={'request': request})
        return Response(serializer.data)

class EventUserSerializer(serializers.ModelSerializer):
    """JSON serializer for event coach's related Django user"""
    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'email']

class EventCoachSerializer(serializers.ModelSerializer):
    """Json serializer for event coach"""

    class Meta:
        model = Coach
        fields = ['user']

class TeamSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for teams"""
    class Meta:
        model: Team
        fields = ('id', 'team_name', 'team_type', 'team_rank', 'team_value', 'team_rerolls', 'fan_factor', 'league_name')

class EventSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for events"""

    class Meta:
        model = Event
        url = serializers.HyperlinkedIdentityField(
            view_name='event',
            lookup_field='id'
        )
        fields = ('id', 'url', 'day', 'time', 'location', 'final_score', 'event_schedule')
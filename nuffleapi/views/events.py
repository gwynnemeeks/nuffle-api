"""View module for handling requests about players"""

from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from nuffleapi.models import Coach, Event

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

    def create(self, request):
        """Handles POST opoerations

        Returns:
            Response -- JSON serialized team instance
        """

        # Uses the token passed in the `Authorization` header
        coach = Coach.objects.get(user=request.auth.user)

        # Create new instance of the Event class and set its properties
        event = Event()
        event.day = request.data["day"]
        event.time = request.data["time"]
        event.location = request.data["location"]
        event.final_score = request.data["final_score"]
        event.event_schedule = request.data["event_schedule"]
        event.coach = coach

        # try to save the new event to the database
        # serialize the event instance as JSON
        # send JSON as a response to the client
        try:
            event.save()
            serializer = EventSerializer(event, context={'request': request})
            return Response(serializer.data)

        # if anything went wrong, catch the exception
        # send a response with 400 status code to tell the client
        # something was wrong with its request data
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)


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

class EventSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for events"""

    coach = EventCoachSerializer(many=False)

    class Meta:
        model = Event
        url = serializers.HyperlinkedIdentityField(
            view_name='event',
            lookup_field='id'
        )
        fields = ('id', 'url', 'day', 'time', 'location', 'final_score', 'event_schedule', 'coach')
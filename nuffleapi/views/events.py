"""View module for handling requests about players"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from nuffleapi.models import Event

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
        Events = Event.objects.all()

        # Note the addtional `many=True` argument to the
        # serializer. It's needed when you are serializing
        # a list of objects instead of a single object.
        serializer = EventSerializer(
            Events, many=True, context={'request': request})
        return Response(serializer.data)

class EventSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for events

    Arguments:
        serializers
    """
    class Meta:
        model = Event
        url = serializers.HyperlinkedIdentityField(
            view_name='event'
            lookup_field='id'
        )
        fields = ('id', 'day', 'time', 'location', 'final_score', 'event_schedule')
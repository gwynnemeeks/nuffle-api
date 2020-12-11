"""View module for handling requests about eventteams"""
from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from nuffleapi.models import EventNote, eventnotes
from nuffleapi.views.events import EventSerializer

class EventNotes(ViewSet):

    """ eventteam viewset"""
    def retrieve(self, request, pk=None):
        """Handle GET requests for event team
        Returns:
            Response -- JSON serialized event team instance
        """
        try:
            # `pk` is a parameter to this function, and
            # Django parses it from the URL route parameter
            #   http://localhost:8000/eventnotes/2
            #
            # The `2` at the end of the route becomes `pk`

            eventnotes = EventNote.objects.get(pk=pk)
            serializer = eventNoteSerializer(eventnotes, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """Handle GET requests to eventteams resource
        Returns:
            Response -- JSON serialized list of games
        """
        # Get all event teams records from the database
        eventnotes = EventNote.objects.all()

        serializer = eventNoteSerializer(
            eventnotes, many=True, context={'request': request})
        return Response(serializer.data)

class eventNoteSerializer(serializers.ModelSerializer):
    """JSON serializer for event teams"""

    event = EventSerializer(many=False)

    class Meta:
        model = EventNote
        fields = ('id', 'event', 'notes')
        depth = 1
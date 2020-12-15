"""View module for handling requests about eventteams"""
from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from nuffleapi.models import EventNote, Event
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
            Response -- JSON serialized list of eventNotess
        """
        # Get all event teams records from the database
        eventnotes = EventNote.objects.all()

        serializer = eventNoteSerializer(
            eventnotes, many=True, context={'request': request})
        return Response(serializer.data)

    def create(self, request):
        """handles POST operation

        Returns:
            Response -- JSON serialized eventteams instance
        """
        
        # Create a new instance of the EventTeam class
        # and set its properties from what was sent in 
        # the body of the requet from the client.

        eventNotes = EventNote()
        event = Event.objects.get(pk=request.data["event_id"])
        
        eventNotes.event = event
        eventNotes.notes = request.data["notes"]

        try:
            eventNotes.save()
            serializer = eventNoteSerializer(eventNotes, context={'request': request})
            return Response(serializer.data)

        # If anything went wrong, catch the exception and
        # send a response with a 400 status code to tell the
        # client that something was wrong with its request data
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single eventNotes

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            eventNotes = EventNote.objects.get(pk=pk)
            eventNotes.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except EventNote.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class eventNoteSerializer(serializers.ModelSerializer):
    """JSON serializer for event teams"""

    event = EventSerializer(many=False)

    class Meta:
        model = EventNote
        fields = ('id', 'event', 'notes')
        depth = 1
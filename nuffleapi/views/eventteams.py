"""View module for handling requests about eventteams"""
from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from nuffleapi.models import EventTeam, Event, Team
from nuffleapi.views.events import EventSerializer
from nuffleapi.views.teams import TeamSerializer


class EventTeams(ViewSet):

    """ eventteam viewset"""
    def retrieve(self, request, pk=None):
        """Handle GET requests for event team
        Returns:
            Response -- JSON serialized event team instance
        """
        try:
            # `pk` is a parameter to this function, and
            # Django parses it from the URL route parameter
            #   http://localhost:8000/eventteams/2
            #
            # The `2` at the end of the route becomes `pk`

            eventteam = EventTeam.objects.get(pk=pk)
            serializer = eventTeamSerializer(eventteam, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """Handle GET requests to eventteams resource
        Returns:
            Response -- JSON serialized list of eventTeams
        """
        # Get all event teams records from the database
        eventteams = EventTeam.objects.all()

        serializer = eventTeamSerializer(
            eventteams, many=True, context={'request': request})
        return Response(serializer.data)

    def create(self, request):
        """handles POST operation

        Returns:
            Response -- JSON serialized eventteams instance
        """
        
        # Create a new instance of the EventTeam class
        # and set its properties from what was sent in 
        # the body of the requet from the client.

        eventTeam = EventTeam()
        event = Event.objects.get(pk=request.data["event_id"])
        team = Team.objects.get(pk=request.data["team_id"])
        eventTeam.event = event
        eventTeam.team = team

        try:
            eventTeam.save()
            serializer = eventTeamSerializer(eventTeam, context={'request': request})
            return Response(serializer.data)

        # If anything went wrong, catch the exception and
        # send a response with a 400 status code to tell the
        # client that something was wrong with its request data
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single eventTeam

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            eventTeam = EventTeam.objects.get(pk=pk)
            eventTeam.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except EventTeam.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class eventTeamSerializer(serializers.ModelSerializer):
    """JSON serializer for event teams"""

    event = EventSerializer(many=False)
    team = TeamSerializer(many=False)

    class Meta:
        model = EventTeam
        fields = ('id', 'event', 'team')
        depth = 1
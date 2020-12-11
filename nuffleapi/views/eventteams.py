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
            Response -- JSON serialized list of games
        """
        # Get all event teams records from the database
        eventteams = EventTeam.objects.all()

        serializer = eventTeamSerializer(
            eventteams, many=True, context={'request': request})
        return Response(serializer.data)

class eventTeamSerializer(serializers.ModelSerializer):
    """JSON serializer for event teams"""

    event = EventSerializer(many=False)
    team = TeamSerializer(many=False)

    class Meta:
        model = EventTeam
        fields = ('id', 'event', 'team')
        depth = 1
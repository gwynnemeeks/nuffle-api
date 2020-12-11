"""View module for handling requests about event-teams"""

from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from nuffleapi.models import EventTeam
from nuffleapi.views.events import EventSerializer
from nuffleapi.views.teams import TeamSerializer


class EventTeams(ViewSet):
    """Nuffle event-teams"""

    def retrieve(self, request, pk=None):
        """Handle GET requests for single event-teams

        Returns:
            Response -- JSON serialized event-teams
        """
        try:
            event_teams = EventTeam.objects.get(pk=pk)
            serializer = EventTeamSerializer(event_teams, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """Handle GET requests to get all event-teams

        Returns:
            Response -- JSON serialized list of event-teams
        """
        event_teams = EventTeam.objects.all()

        # Note the addtional `many=True` argument to the
        # serializer. It's needed when you are serializing
        # a list of objects instead of a single object.
        serializer = EventTeamSerializer(
            event_teams, many=True, context={'request': request})
        return Response(serializer.data)

class EventTeamSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for game types

    Arguments:
        serializers
    """

    event = EventSerializer(many=True)
    team = TeamSerializer(many=True)

    class Meta:
        model = EventTeam
        url = serializers.HyperlinkedIdentityField(
            view_name='eventteam',
            lookup_field='id'
        )
        fields = ('id', 'event', 'team')
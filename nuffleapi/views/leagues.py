"""View module for handling requests about leagues"""

from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError

from rest_framework import serializers
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from nuffleapi.models import League
from nuffleapi.views.coach import CoachProfileSerializer
from nuffleapi.views.teams import TeamSerializer

class Leagues(ViewSet):
    """Nuffle Leagues"""

    def retrieve(self, request, pk=None):
        """Handle GET requests for single league

        Returns:
            Response -- JSON serialized league
        """
        try:
            leagues = League.objects.get(pk=pk)
            serializer = LeagueSerializer(leagues, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """Handle GET requests to the leagues resource
        
        Returns:
            Response == JSON serialized list of leagues
        """
        # Get all team records from the database
        leagues = League.objects.all()

        serializer = LeagueSerializer (
            leagues, many=True, context={'request': request})
        return Response(serializer.data)

class LeagueSerializer(serializers.HyperlinkedModelSerializer):
    """Json serializer for leagues

    Arguments:
        serializer type
    """

    coach = CoachProfileSerializer(many=False)

    class Meta:
        model = League
        url = serializers.HyperlinkedIdentityField(
            view_name='leagues',
            lookup_field='id'
        )
        fields = ('id', 'coach', 'teams')
        depth = 1
"""View module for handling requests about leagues"""

from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError

from rest_framework import serializers
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from nuffleapi.models import League
from nuffleapi.views.coach import Coach, CoachProfileSerializer

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

    def create(self, request):
        """Handles POST opoerations

        Returns:
            Response -- JSON serialized team instance
        """

        # Uses the token passed in the `Authorization` header
        coach = Coach.objects.get(user=request.auth.user)

        # Create new instance of the League class and set its properties
        league = League()
        league.league_name = request.data["league_name"]

        league.coach = coach

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
        fields = ('id', 'coach', 'league_name', 'teams')
        depth = 1
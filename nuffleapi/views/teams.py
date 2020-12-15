"""View module for handling requests about teams"""

from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError

from rest_framework import serializers
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from nuffleapi.models import Team
from nuffleapi.views.coach import Coach, CoachProfileSerializer
from nuffleapi.views.leagues import League, LeagueSerializer

class Teams(ViewSet):
    """Nuffle teams"""

    def retrieve(self, request, pk=None):
        """Handle GET requests for single team

        Returns:
            Response -- JSON serialized team
        """
        try:
            teams = Team.objects.get(pk=pk)
            serializer = TeamSerializer(teams, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """Handle GET requests to the teams resource
        
        Returns:
            Response == JSON serialized list of teams
        """
        # Get all team records from the database
        teams = Team.objects.all()

        serializer = TeamSerializer (
            teams, many=True, context={'request': request})
        return Response(serializer.data)

    def create(self, request):
        """Handles POST opoerations

        Returns:
            Response -- JSON serialized team instance
        """

        # Uses the token passed in the `Authorization` header
        coach = Coach.objects.get(user=request.auth.user)
        league = League.objects.get(pk=request.data["league_id"])

        # Create new instance of the Team class and set its properties
        team = Team()
        team.team_name = request.data["team_name"]
        team.team_type = request.data["team_type"]
        team.team_rank = request.data["team_rank"]
        team.team_value = request.data["team_value"]
        team.team_rerolls = request.data["team_rerolls"]
        team.fan_factor = request.data["fan_factor"]

        team.coach = coach
        team.league = league

        # try to save the new team to the database
        # serialize the team instance as JSON 
        # send JSON as a response to the client request 
        try:
            team.save()
            serializer = TeamSerializer(team, context={'request': request})
            return Response(serializer.data)

        # if anything went wrong, catch the exception
        # send a response with 400 status code to tell the client
        # something was wrong with its request data
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)


class TeamSerializer(serializers.HyperlinkedModelSerializer):
    """Json serializer for teams

    Arguments:
        serializer type
    """

    coach = CoachProfileSerializer(many=False)
    league = LeagueSerializer(many=False)

    class Meta:
        model = Team
        url = serializers.HyperlinkedIdentityField(
            view_name='teams',
            lookup_field='id'
        )
        fields = ('id', 'coach', 'team_name', 'team_type', 'team_rank', 'team_value', 'team_rerolls', 'fan_factor', 'league')
        depth = 1
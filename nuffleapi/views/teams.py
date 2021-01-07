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

        coach = Coach.objects.get(user=request.auth.user)
        if coach is not None:
            teams = teams.filter(coach=coach)

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
        # Matches the league_id to the team
        league = League.objects.get(pk=request.data["leagueId"])

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

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single team

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            team = Team.objects.get(pk=pk)
            team.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Team.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, pk=None):
        """Handle PUT requests for a game

        Returns:
            Response -- Empty body with 204 status code
        """
        # Uses the token passed in Auth header
        coach = Coach.objects.get(user=request.auth.user)
            
        # Do mostly the same thing as POST, but instead of
        # creating a new instance of Game, get the game record
        # from the database whose primary key is `pk`
        team = Team.objects.get(pk=pk)
        team.team_name = request.data["teamName"]
        team.team_type = request.data["teamType"]
        team.team_rank = request.data["teamRank"]
        team.team_value = request.data["teamValue"]
        team.team_rerolls = request.data["teamRerolls"]
        team.fan_factor = request.data["fanFactor"]
        team.coach = coach

        league = League.objects.get(pk=int(request.data["leagueId"]))
        team.league = league
        team.save()

        # 204 status code means everything worked but the
        # server is not sending back any data in the response
        return Response({}, status=status.HTTP_204_NO_CONTENT)


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
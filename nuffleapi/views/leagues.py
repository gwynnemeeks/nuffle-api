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
        league.league_name = request.data["leagueName"]

        league.coach = coach

         # try to save the new league to the database
        # serialize the league instance as JSON 
        # send JSON as a response to the client request 
        try:
            league.save()
            serializer = LeagueSerializer(league, context={'request': request})
            return Response(serializer.data)

        # if anything went wrong, catch the exception
        # send a response with 400 status code to tell the client
        # something was wrong with its request data
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single league

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            league = League.objects.get(pk=pk)
            league.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except League.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, pk=None):
        """Handle PUT requests for a game

        Returns:
            Response -- Empty body with 204 status code
        """

        coach = Coach.objects.get(user=request.auth.user)

        # Do mostly the same thing as POST, but instead of
        # creating a new instance of Game, get the game record
        # from the database whose primary key is `pk`

        league = League.objects.get(pk=pk)
        league.league_name = request.data["leagueName"]

        league.coach = coach
        league.save()

        # 204 status code means everything worked but the
        # server is not sending back any data in the response
        return Response({}, status=status.HTTP_204_NO_CONTENT)

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
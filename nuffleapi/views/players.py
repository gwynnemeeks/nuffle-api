"""View module for handling requests about players"""

from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError

from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status

from nuffleapi.models import Player, Team
from nuffleapi.views.teams import TeamSerializer

class Players(ViewSet):
    """Nuffle players"""

    def retrieve(self, request, pk=None):
        """Handle GET requests for single player

        Returns:
            Response -- JSON serialized player
        """
        try:
            player = Player.objects.get(pk=pk)
            serializer = PlayerSerializer(player, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """Handle GET requests to get all players

        Returns:
            Response -- JSON serialized list of players
        """
        Players = Player.objects.all()

        # Note the addtional `many=True` argument to the
        # serializer. It's needed when you are serializing
        # a list of objects instead of a single object.
        serializer = PlayerSerializer(
            Players, many=True, context={'request': request})
        return Response(serializer.data)

    def create(self, request):
        """Handles POST opoerations

        Returns:
            Response -- JSON serialized player instance
        """

        # Uses the token passed in the `Authorization` header
        team = Team.objects.get(user=request.auth.user)

        # Create new instance of the player class and set its properties
        player = Player()
        player.team = team
        player.name = request.data["name"]
        player.position = request.data["position"]
        player.movement = request.data["movement"]
        player.strength = request.data["strength"]
        player.agility = request.data["agility"]
        player.armor_value = request.data["armor_value"]
        player.skills = request.data["skills"]
        player.cost = request.data["cost"]
        player.history = request.data["history"]


        # try to save the new player to the database
        # serialize the player instance as JSON 
        # send JSON as a response to the client request 
        try:
            player.save()
            serializer = PlayerSerializer(player, context={'request': request})
            return Response(serializer.data)

        # if anything went wrong, catch the exception
        # send a response with 400 status code to tell the client
        # something was wrong with its request data
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

class PlayerSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for players

    Arguments:
        serializers
    """
    team = TeamSerializer(many=False)

    class Meta:
        model = Player
        url = serializers.HyperlinkedIdentityField(
            view_name='player',
            lookup_field='id'
        )
        fields = ('id', 'team', 'name', 'position', 'movement', 'strength', 'agility', 'armor_value', 'skills', 'cost', 'history')
        depth = 1
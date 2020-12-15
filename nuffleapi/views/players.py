"""View module for handling requests about players"""

from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError

from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status

from nuffleapi.models import Player, Team
from nuffleapi.views.players import playerSerializer

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
        players = Player.objects.all()

        # Note the addtional `many=True` argument to the
        # serializer. It's needed when you are serializing
        # a list of objects instead of a single object.
        serializer = PlayerSerializer(
            players, many=True, context={'request': request})
        return Response(serializer.data)

    def create(self, request):
        """Handles POST opoerations

        Returns:
            Response -- JSON serialized player instance
        """

        # Figure out that auth stuff and add it back in

        player = Player.objects.get(pk=request.data["player_id"])
        team = Team.objects.get(pk=request.data["team_id"])

        #Create a new instance of the Player class and set its properties
        player = Player()

        player.name = request.data["name"]
        player.position = request.data["position"]
        player.movement = request.data["movement"]
        player.strength = request.data["strength"]
        player.agility = request.data["agility"]
        player.armor_value = request.data["armor_value"]
        player.skills = request.data["skills"]
        player.cost = request.data["cost"]
        player.history = request.data["history"]
        player.team = team
        player.player = player


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

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single player

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            player = Player.objects.get(pk=pk)
            player.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Player.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PlayerSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for players

    Arguments:
        serializers
    """
    player = playerSerializer(many=False)

    class Meta:
        model = Player
        url = serializers.HyperlinkedIdentityField(
            view_name='player',
            lookup_field='id'
        )
        fields = ('id', 'player', 'name', 'position', 'movement', 'strength', 'agility', 'armor_value', 'skills', 'cost', 'history')
        depth = 1
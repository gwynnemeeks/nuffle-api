"""View module for handling requests about players"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from nuffleapi.models import Player

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

class PlayerSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for players

    Arguments:
        serializers
    """
    class Meta:
        model = Player
        url = serializers.HyperlinkedIdentityField(
            view_name='player',
            lookup_field='id'
        )
        fields = ('id', 'url', 'team', 'name', 'position', 'movement', 'strength', 'agility', 'armor_value', 'skills', 'cost', 'history')
        depth = 1
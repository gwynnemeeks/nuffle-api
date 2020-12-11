"""View module for handling requests about teams"""

from django.core.exceptions import ValidationError
from django.db.models import fields
from django.http import HttpResponseServerError

from rest_framework import serializers
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from nuffleapi.models import Team
from nuffleapi.views.coach import CoachUser

class Teams(ViewSet):
    """Nuffle teams"""

    def list (self, request):
        """Handle GET requests to the teams resource
        
        Returns:
            Response == JSON serialized list of teams
        """
        # Get all team records from the database
        teams = Team.objects.all()

        serializer = TeamSerializer (
            teams, many=True, context={'request': request})
        return Response(serializer.data)

class TeamSerializer(serializers.HyperlinkedModelSerializer):
    """Json serializer for teams

    Arguments:
        serializer type
    """
    class Meta:
        model = Team
        url = serializers.HyperlinkedIdentityField(
            view_name='teams',
            lookup_field='id'
        )
        fields = ('id', 'team_name', 'team_type', 'team_rank', 'team_value', 'team_rerolls', 'fan_factor', 'league_name')
        depth = 1
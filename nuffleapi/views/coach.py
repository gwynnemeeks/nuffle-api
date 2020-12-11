"""View module for handling requests about coaches"""
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.db.models import fields
from django.http import HttpResponseServerError
from django.http import request

from rest_framework import serializers
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from nuffleapi.models import Coach

class CoachUser(ViewSet):

    def retrieve(self, request, pk=None):
        """Hangle GET request for single coach

        Returns:
            Response -- JSON serialized coach instance
        """

        try:
            user = Coach.objects.get(pk=pk)
            serializer = CoachProfileSerializer(user, context={'request': request})
            return Response(serializer.data)

        except Exception as ex:
            return HttpResponseServerError(ex)

class CoachUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name')

class CoachProfileSerializer(serializers.ModelSerializer):

    user = CoachUserSerializer(many=False)

    class Meta:
        model = Coach
        fields = ('id', 'title', 'user')
        depth = 1
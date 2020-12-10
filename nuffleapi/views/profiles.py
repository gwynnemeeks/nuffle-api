from django.http import request
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from nuffleapi.models import Coach

from django.contrib.auth.models import User


class Profile(ViewSet):
    
    def list(self, request):
            """Handle get requests for profiles """
            profiles = Coach.objects.all().order_by('user')
            serializer = ProfileSerializer(profiles, many=True, context={'request': request})
            return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single post
        Returns:
            Response -- JSON serialized game instance
        """
        
        try:
            user = User.objects.get(pk=pk)
            serializer = ProfileUserSerializer(user, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """Handle PUT requests for a Post
        Returns:
            Response -- Empty body with 204 status code
        """

        coach = Coach.objects.get(user=request.auth.user)

        # Do mostly the same thing as POST, but instead of 
        # creating a new instance of Post, get the post record
        # from the database whose primary key is `pk`
        user = Coach.objects.get(pk=pk)

        # user.active = request.data['active']
        # if user.active == False:
        #     user.active = True
        # else: 
        #     user.active = False
        user.save()

        # 204 status code means everything worked by the
        # server is not sending back any data in the response

        return Response({}, status=status.HTTP_204_NO_CONTENT)

class ProfileUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name')

class ProfileSerializer(serializers.ModelSerializer):
    
    user = ProfileUserSerializer(many=False)

    class Meta:
        model = Coach
        
        fields = ('id', 'title', 'user')
        depth = 1
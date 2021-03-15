"""View module for handling requests about games"""
from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from readAloudapi.models import Book
from rest_framework.decorators import action
from readAloudapi.models.profile import Profile
from django.contrib.auth.models import User


class Profiles(ViewSet):
    """Read Aloud Profiles"""

    def list(self, request):
        """Handle GET requests to profile resource

        Returns:
            Response -- JSON serialized list of profiles
        """        

        profiles = Profile.objects.all()

        serializer = ProfileSerializer(
            profiles, many=True, context={'request':request})
        return Response(serializer.data)

    # def retrieve(self, request, pk=None):
    #     """Handle GET requests for single tag

    #     Returns:
    #         Response -- JSON serialized tag instance
    #     """

    #     if pk == None:
    #         active_user = Profile.objects.get(user=request.auth.user)
    #     else:
    #         active_user = Profile.objects.get(pk=pk)
     
    #     serializer = ProfileSerializer(active_user, context={'request': request}, many=False)
    #     return Response(serializer.data)

    @action(methods=['GET',], detail=True)
    def current_profile(self, request):
        """Handle GET requests to profile resource

        Returns:
            Response -- JSON representation of user info
        """

        profile = Profile.objects.get(user=request.auth.user)

        profile = ProfileSerializer(profile, many=False, constext={'request': request})

        return Response(profile)


class UserSerializer(serializers.ModelSerializer):
    """JSON serializer for Users

    Arguments:
        serializer type
    """   

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name')

class ProfileSerializer(serializers.ModelSerializer):
    """JSON serializer for Profiles

    Arguments:
        serializer type
    """

    user = UserSerializer(many=False)

    class Meta:
        model = Profile
        fields =('id', 'user', 'bio', 'role', 'profile_pic')
        depth = 1
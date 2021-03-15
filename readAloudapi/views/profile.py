"""View module for handling requests about games"""
from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework import viewsets
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from readAloudapi.models import Book
from rest_framework.decorators import action
from readAloudapi.models.profile import Profile
from django.contrib.auth.models import User
from readAloudapi.views.profiles import ProfileSerializer

class ProfilePage(ViewSet):
    def list(self, request):
        """Handle GET requests to profile resource

        Returns:
            Response -- JSON serialized list of profiles
        """        
        profile = Profile.objects.get(user=request.auth.user)

        serializer = ProfileSerializer(
            profile, many=False, context={'request':request})
        return Response(serializer.data)

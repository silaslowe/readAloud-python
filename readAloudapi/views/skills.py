"""View module for handling requests about games"""
from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from readAloudapi.models.skill import Skill

class Skills(ViewSet):
    """Read Aloud vocab"""

    def create(self, request):

        """Handle POST operations

        Returns:
            Response -- JSON serialized vocab instance
        """

        skill = Skill()
        skill.skill = request.data['skill']

        # Try to save the new game to the database, then
        # serialize the game instance as JSON, and send the
        # JSON as a response to the client request

        try:
            skill.save()
            serializer = SkillSerializer(skill, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED) 

        # If anything went wrong, catch the exception and
        # send a response with a 400 status code to tell the
        # client that something was wrong with its request data   

        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

class SkillSerializer(serializers.ModelSerializer):
    """JSON serializer for vocab

    Arguments:
        serializer type
    """    

    class Meta:
        model = Skill
        fields = ('id', 'skill')
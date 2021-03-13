"""View module for handling requests about games"""
from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from readAloudapi.models.book import Book
from readAloudapi.models.skill import Skill
from readAloudapi.models.book_skill import BookSkill

class Skills(ViewSet):
    """Read Aloud Skills"""

    def create(self, request):

        """Handle POST operations

        Returns:
            Response -- JSON serialized vocab instance
        """

        # Gets book from request.data
        book = Book.objects.get(pk=request.data['bookId'])
        
        try:
            # Attempts to get skill from db. 
            skill = Skill.objects.get(skill=request.data['skill'])

        except Skill.DoesNotExist:

            # If skill not in db creates a new instance of the skill model
            skill = Skill()
            # Adds a skill property to the instance
            skill.skill= request.data['skill']
            # Create ORM
            skill.save()

        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)
        
        # Creates a relationship object between the current book and the skill
        bookskill = BookSkill() 
        bookskill.book = book
        bookskill.skill = skill
        bookskill.save()

        # Serializes the skill data to send to the client in the response    
        serializer = SkillSerializer(skill, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)


    def list(self, request):

        """Handle GET requests to games resource

        Returns:
            Response -- JSON serialized list of games
        """

        skills = Skill.objects.all()

        serializer = SkillSerializer(skills, many=True, context={'request': request})
        return Response(serializer.data)

class SkillSerializer(serializers.ModelSerializer):
    """JSON serializer for vocab

    Arguments:
        serializer type
    """    

    class Meta: 
        model = Skill
        fields = ('id', 'skill')
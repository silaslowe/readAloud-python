"""View module for handling requests about games"""
from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rest_framework.decorators import action
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

        try:
            # Attempts to get skill from db. 
            bookskill = BookSkill.objects.get(skill=skill, book = book)

        except BookSkill.DoesNotExist:

            # Creates a relationship object between the current book and the skill

            bookskill = BookSkill() 
            bookskill.book = book
            bookskill.skill = skill
            bookskill.save()

        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)
        

        # Serializes the skill data to send to the client in the response    
        serializer = SkillSerializer(skill, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(methods=['POST'], detail=False)
    def get_skills_by_book(self, request):
        """Handle GET skills by book

        Returns:
            Response -- JSON serialized list of skills
        """

        book = Book.objects.get(pk=request.data["bookId"])
        skills = Skill.objects.filter(books__book_id = book.id)

        serializer = SkillSerializer(skills, many=True, context={'request': request})

        return Response(serializer.data)

    @action(methods=['DELETE'], detail=False)
    def destroy_skill_book_relationship(self, request):
        """Handle DELETE skills/book releationship"""

        book = Book.objects.get(pk=request.data["bookId"])
        skill = Skill.objects.get(pk=request.data["skillId"])
        book_skill_rel = BookSkill.objects.all().filter(book_id = book.id, skill_id = skill.id)

        book_skill_rel.delete()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

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
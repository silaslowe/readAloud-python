"""View module for handling requests about games"""
from readAloudapi.models.question import Question
from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from readAloudapi.models import Book

class Questions(ViewSet):
    """Read Aloud books"""

    def create(self, request, pk=None):
        """Handle POST operations

        Returns:
            Response -- JSON serialized book instance
        """
        book = Book.objects.get(pk=request.data["bookId"])
        question = Question()
        question.book = book 
        question.question = request.data["question"]
        question.page = request.data["page"]

        try:
            question.save()
            serializer = QuestionSerializer(question, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)



class QuestionSerializer(serializers.ModelSerializer):
    """JSON serializer for questions

    Arguments:
        serializer type
    """

    class Meta:
        model = Question
        fields =('id', 'question', 'page', 'book')
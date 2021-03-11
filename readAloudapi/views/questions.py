"""View module for handling requests about games"""
from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from readAloudapi.models import Book
from readAloudapi.models.question import Question

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

    def list(self, request):
        """Handle GET requests to question resource

        Returns:
            Response -- JSON serialized list of questions
        """        

        questions = Question.objects.all()

        serializer = QuestionSerializer(
            questions, many=True, context={'request':request})
        return Response(serializer.data)


    def destroy(self, request, pk=None):

        """Handle DELETE requests for a single question

        Returns:
            Response -- 200, 404, or 500 status code
        """

        try: 
            question = Question.objects.get(pk=pk)
            question.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Question.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def update(self, request, pk=None):
        """Handle PUT requests for a question

        Returns:
            Response -- Empty body with 204 status code
        """        

        # book = Book.objects.get(pk=request.data["bookId"])

        # Does mostly the same thing as POST, but instead of
        # creating a new instance of Question, get the question record
        # from the database whose primary key is `pk`

        question = Question.objects.get(pk=pk)
        question.question = request.data['question']
        question.page = request.data['page']
        question.book = Book.objects.get(pk=request.data["bookId"])

        #ORM for PUT method

        question.save()

        # 204 status code means everything worked but the
        # server is not sending back any data in the response

        return Response({}, status=status.HTTP_204_NO_CONTENT)


class QuestionSerializer(serializers.ModelSerializer):
    """JSON serializer for questions

    Arguments:
        serializer type
    """

    class Meta:
        model = Question
        fields =('id', 'question', 'page', 'book')
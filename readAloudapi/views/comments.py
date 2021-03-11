"""View module for handling requests about games"""
from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from readAloudapi.models.comment import Comment
from readAloudapi.models.book import Book
from readAloudapi.models.profile import Profile
from datetime import date




class Comments(ViewSet):
    """Read Aloud Book Guide Comments"""

    def create(self, request):

        """Handle POST operations

        Returns:
            Response -- JSON serialized vocab instance
        """

        book = Book.objects.get(pk=request.data['bookId'])
        profile = Profile.objects.get(user=request.auth.user)
        today = date.today()


        comment = Comment()
        comment.comment = request.data['comment']
        comment.book = book
        comment.profile = profile
        comment.created_on = today

        # Try to save the new game to the database, then
        # serialize the game instance as JSON, and send the
        # JSON as a response to the client request

        try:
            comment.save()
            serializer = CommentSerializer(comment, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED) 

        # If anything went wrong, catch the exception and
        # send a response with a 400 status code to tell the
        # client that something was wrong with its request data   

        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):

        """Handle GET requests to games resource

        Returns:
            Response -- JSON serialized list of games
        """

        comments = Comment.objects.all()

        serializer = CommentSerializer(comments, many=True, context={'request': request})
        return Response(serializer.data)

class CommentSerializer(serializers.ModelSerializer):
    """JSON serializer for vocab

    Arguments:
        serializer type
    """    

    class Meta: 
        model = Comment
        fields = ('id', 'comment', 'book', 'profile', 'created_on')

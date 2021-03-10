"""View module for handling requests about games"""
from readAloudapi.models.book import Book
from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from readAloudapi.models import Profile


class Books(ViewSet):
    """Read Aloud books"""

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized book instance
        """

        # Uses the token passed in the `Authorization` header

        profile = Profile.objects.get(user=request.auth.user)

        # Create a new Python instance of the Book class
        # and set its properties from what was sent in the
        # body of the request from the client.

        book = Book()
        book.profile = profile
        book.title = request.data["title"]
        book.author = request.data["author"]
        book.publish_year =request.data["publishYear"]
        book.notes = request.data["notes"]
        book.cover_url = request.data["coverUrl"] 
        book.rating = request.data["rating"]
        book.location = request.data["location"]
        book.synopsis = request.data["synopsis"]


        # Try to save the new book to the database, then
        # serialize the book instance as JSON, and send the
        # JSON as a response to the client request

        try:
            book.save()
            serializer = BookSerializer(book, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        # If anything went wrong, catch the exception and
        # send a response with a 400 status code to tell the
        # client that something was wrong with its request data

        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        """Handle GET requests to books resource

        Returns:
            Response -- JSON serialized list of books
        """

        books = Book.objects.all()

        serializer = BookSerializer(
            books, many=True, context={'request': request})

        return Response(serializer.data)

class BookSerializer(serializers.ModelSerializer):
    """JSON serializer for books

    Arguments:
        serializer type
    """

    class Meta:
        model = Book
        fields = ('id', 'title', 'author', 'publish_year', 'notes', 'cover_url', 'rating', 'location', 'synopsis')

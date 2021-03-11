"""View module for handling requests about games"""
from readAloudapi.models.book import Book
from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from django.db.models import F
from readAloudapi.models import Profile, Topic, BookTopic, book_topic


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

    def retrieve(self, request, pk=None):
        """Handle GET requests for single book

        Returns:
            Response -- JSON serialized book instance
        """

        try:
            # `pk` is a parameter to this function, and
            # Django parses it from the URL route parameter
            #   http://localhost:8000/books/2
            #
            # The `2` at the end of the route becomes `pk`


            book = Book.objects.get(pk=pk)
            # Get all topics, filter to join booktopic on topic id = F(gets the topics that are in use or attached to a book) =>   


            topics = Topic.objects.all().filter(booktopic__book_id = book.id)
            print(topics.query)
            topic_serializer = TopicSerializer(topics, context={'request': request}, many=True)

            serializer = BookSerializer(book, context={'request': request})
            d = {}
            d.update(serializer.data)

            d['topics']=topic_serializer.data


            return Response(d)
        except Book.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return HttpResponseServerError(ex)

class TopicSerializer(serializers.ModelSerializer):
    """JSON serializer for topics

    Arguments:
        serializer type
    """ 

    class Meta:
        model = Topic
        fields = ('topic',) 

# class BookTopicSerializer(serializers.ModelSerializer):
#     """JSON serializer for a book's topics

#     Arguments:
#         serializer type
#     """ 

#     # topic = TopicSerializer(many=True)

#     class Meta:
#         model = BookTopic   
#         fields = ('topic',)
#         depth = 1

class BookSerializer(serializers.ModelSerializer):
    """JSON serializer for books

    Arguments:
        serializer type
    """

    # topic = TopicSerializer(many=True)
    
    class Meta:
        model = Book
        fields = ('id', 'title', 'author', 'publish_year', 'notes', 'cover_url', 'rating', 'location', 'synopsis')
        depth = 1

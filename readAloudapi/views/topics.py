"""View module for handling requests about games"""
from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from readAloudapi.models.book import Book
from readAloudapi.models.topic import Topic
from readAloudapi.models.book_topic import BookTopic

class Topics(ViewSet):
    """Read Aloud vocab"""

    def create(self, request):

        """Handle POST operations

        Returns:
            Response -- JSON serialized vocab instance
        """

        # Gets book from request.data
        book = Book.objects.get(pk=request.data['bookId'])

        try:
            # Attempts to get topic from db. 
            topic = Topic.objects.get(topic=request.data['topic'])


        except Topic.DoesNotExist:

            # If skill not in db creates a new instance of the skill model
            topic = Topic()
            # Adds a skill property to the instance
            topic.topic = request.data['topic']
            # Create ORM
            topic.save()

        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

        # Creates a relationship object between the current book and the topic
        booktopic = BookTopic()
        booktopic.book=book
        booktopic.topic=topic
        booktopic.save()


        # Serializes the skill data to send to the client in the response 
        serializer = TopicSerializer(topic, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)


    def list(self, request):

        """Handle GET requests to games resource

        Returns:
            Response -- JSON serialized list of games
        """

        topics = Topic.objects.all()

        serializer = TopicSerializer(topics, many=True, context={'request': request})
        return Response(serializer.data)

class TopicSerializer(serializers.ModelSerializer):
    """JSON serializer for vocab

    Arguments:
        serializer type
    """    

    class Meta: 
        model = Topic
        fields = ('id', 'topic')
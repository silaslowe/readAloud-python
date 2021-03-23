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

        try:
            # Attempts to get skill from db. 
            bookstopic = BookTopic.objects.get(topic = topic, book = book)

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except BookTopic.DoesNotExist:

        # Creates a relationship object between the current book and the topic

            booktopic = BookTopic() 
            booktopic.book = book
            booktopic.topic = topic
            booktopic.save()

        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

        # Serializes the topic data to send to the client in the response 
        serializer = TopicSerializer(topic, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(methods=['POST'], detail=False)
    def get_topics_by_book(self, request):
        """Handle GET topics by book

        Returns:
            Response -- JSON serialized list of topics
        """

        book = Book.objects.get(pk=request.data["bookId"])
        topics = Topic.objects.all().filter(books__book_id = book.id)

        serializer = TopicSerializer(topics, many=True, context={'request': request})

        return Response(serializer.data)

    @action(methods=['DELETE'], detail=False)
    def destroy_topic_book_relationship(self, request):
        """Handle DELETE topics/book releationship"""

        book = Book.objects.get(pk=request.data["bookId"])
        topic = Topic.objects.get(pk=request.data["topicId"])
        book_topic_rel = BookTopic.objects.all().filter(book_id = book.id, topic_id = topic.id)

        book_topic_rel.delete()

        return Response({}, status=status.HTTP_204_NO_CONTENT)


    def list(self, request):

        """Handle GET requests to topics resource

        Returns:
            Response -- JSON serialized list of topics
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
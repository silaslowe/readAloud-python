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
from readAloudapi.models import Profile, Topic, Skill, Question, Vocab, book_topic, book_skill


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
        book_list = []
        for book in books:
            # Get all topics, filter to join booktopic on topic id = F(gets the topics that are in use or attached to a book) =>   
            # .filter(booktopic__topic_id=F('id'))

            topics = Topic.objects.all().filter(booktopic__book_id = book.id)
            skills = Skill.objects.all().filter(bookskill__book_id = book.id)
            questions = Question.objects.all().filter(book_id=book.id)
            vocabs = Vocab.objects.all().filter(bookvocab__book_id=book.id)
            print(topics.query)
            question_serializer = QuestionSerializer(questions, context={'request': request}, many=True)
            topic_serializer = TopicSerializer(topics, context={'request': request}, many=True)
            skill_serializer = SkillSerializer(skills, context={'request': request}, many=True)
            vocab_serializer = VocabSerializer(vocabs, context={'request': request}, many=True)
            serializer = BookSerializer(book, context={'request': request})
            d = {}
            d.update(serializer.data)
            d['vocab']=vocab_serializer.data
            d['questions']=question_serializer.data
            d['topics']=topic_serializer.data
            d['skills']=skill_serializer.data
            book_list.append(d)



        return Response(book_list)

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
            # .filter(booktopic__topic_id=F('id'))

            topics = Topic.objects.all().filter(booktopic__book_id = book.id)
            skills = Skill.objects.all().filter(bookskill__book_id = book.id)
            questions = Question.objects.all().filter(book_id=book.id)
            vocabs = Vocab.objects.all().filter(bookvocab__book_id=book.id)

            # print(topics.query)
            question_serializer = QuestionSerializer(questions, context={'request': request}, many=True)
            topic_serializer = TopicSerializer(topics, context={'request': request}, many=True)
            skill_serializer = SkillSerializer(skills, context={'request': request}, many=True)
            vocab_serializer = VocabSerializer(vocabs, context={'request': request}, many=True)
            serializer = BookSerializer(book, context={'request': request})
            d = {}
            d.update(serializer.data)
            d['vocab']=vocab_serializer.data
            d['questions']=question_serializer.data
            d['topics']=topic_serializer.data
            d['skills']=skill_serializer.data

            return Response(d)
        except Book.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return HttpResponseServerError(ex)

class VocabSerializer(serializers.ModelSerializer):
    """JSON serializer for topics

    Arguments:
        serializer type
    """ 

    class Meta:
        model = Vocab
        fields = ('id', 'word', 'page') 

class QuestionSerializer(serializers.ModelSerializer):
    """JSON serializer for topics

    Arguments:
        serializer type
    """ 

    class Meta:
        model = Question
        fields = ('id', 'question', 'page') 

class TopicSerializer(serializers.ModelSerializer):
    """JSON serializer for topics

    Arguments:
        serializer type
    """ 

    class Meta:
        model = Topic
        fields = ('id', 'topic') 

class SkillSerializer(serializers.ModelSerializer):
    """JSON serializer for topics

    Arguments:
        serializer type
    """ 

    class Meta:
        model = Skill
        fields = ('id', 'skill') 


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

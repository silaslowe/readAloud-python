"""View module for handling requests about games"""
import json
from readAloudapi.models.book import Book
from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rest_framework.decorators import action
from django.db.models import F
from readAloudapi.models import Profile, Topic, Skill, Question, Vocab, book_profile, book_topic, book_skill, Book, BookSkill, BookProfile


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
        book.notes = ""
        book.cover_url = request.data["coverUrl"] 
        book.rating = 0
        book.location = ""
        book.synopsis = ""


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

    def update(self, request, pk=None):
        """Handle PUT requests for a book

        Returns:
            Response -- Empty body with 204 status code
        """

        book = Book.objects.get(pk=pk)
        profile = Profile.objects.get(user=request.auth.user)

        book.profile = profile
        book.title = request.data["title"]
        book.author = request.data["author"]
        book.publish_year = book.publish_year
        book.notes = request.data["notes"]
        book.cover_url = book.cover_url 
        book.rating = request.data["rating"]
        book.location = request.data["location"]
        book.synopsis = request.data["synopsis"]

        book.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def list(self, request):
        """Handle GET requests to books resource

        Returns:
            Response -- JSON serialized list of books
        """
        books =[]
        profile = Profile.objects.get(user=request.auth.user) 
        books = Book.objects.exclude(profile = profile)

        searched_skill = self.request.query_params.get('skill', None)
        searched_topic = self.request.query_params.get('topic', None)
        searched_title = self.request.query_params.get('title', None)

        if searched_skill is not None:
            try:
                skill = Skill.objects.get(skill = searched_skill)
                books = books.filter(skills__skill = skill)

            except Book.DoesNotExist as ex:
                books = None
                return Response(books, status=status.HTTP_404_NOT_FOUND)
            # except Exception:
            #     books = None
            #     return Response(books, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
        
        if searched_topic is not None:

            try:        
                topic = Topic.objects.get(topic = searched_topic)
                books = books.filter(topic__topic = topic)

            except Book.DoesNotExist as ex:
                books = None
                return Response(books, status=status.HTTP_404_NOT_FOUND)
            except Exception:
                books = None
                return Response(books, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        if searched_title is not None:
            try:

                books = books.filter(title__contains=searched_title)

            except Book.DoesNotExist as ex:
                books = None
                return Response(books, status=status.HTTP_404_NOT_FOUND)
            except Exception:
                books = None
                return Response(books, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 


        book_list = []
        for book in books:

            # Gets all resources needed from database and filters the relevant rows
            topics = Topic.objects.all().filter(books__book_id = book.id)
            skills = Skill.objects.all().filter(books__book_id = book.id)
            questions = Question.objects.all().filter(book_id=book.id)
            vocabs = Vocab.objects.all().filter(bookvocab__book_id=book.id)

            # Serialize filtered data
            question_serializer = QuestionSerializer(questions, context={'request': request}, many=True)
            topic_serializer = TopicSerializer(topics, context={'request': request}, many=True)
            skill_serializer = SkillSerializer(skills, context={'request': request}, many=True)
            vocab_serializer = VocabSerializer(vocabs, context={'request': request}, many=True)
            serializer = BookSerializer(book, context={'request': request})

           
            # Create an empty dictionary to hold copy of serialized data
            d = {}

            # Copy data into empty dicitonary
            d.update(serializer.data)

            # Add each set of serialized data as a property 
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
            profile = Profile.objects.get(user=request.auth.user) 

            if book.profile_id == profile.id:
                book.is_current_user = True
            else:
                book.is_current_user = False
            # Get all topics, filter to join booktopic on topic id = F(gets the topics that are in use or attached to a book) =>   
            # .filter(booktopic__topic_id=F('id'))

            # Gets all resources needed from database and filters the relevant rows
            topics = Topic.objects.filter(books__book_id = book.id)
            skills = Skill.objects.filter(books__book_id = book.id)
            questions = Question.objects.filter(book_id = book.id)
            vocabs = Vocab.objects.filter(bookvocab__book_id = book.id)

            # Serialize filtered data
            question_serializer = QuestionSerializer(questions, context={'request': request}, many=True)
            topic_serializer = TopicSerializer(topics, context={'request': request}, many=True)
            skill_serializer = SkillSerializer(skills, context={'request': request}, many=True)
            vocab_serializer = VocabSerializer(vocabs, context={'request': request}, many=True)
            serializer = BookSerializer(book, context={'request': request})

            # Create an empty dictionary to hold copy of serialized data
            d = {}

            # Copy data into empty dicitonary
            d.update(serializer.data)

            # Add each set of serialized data as a property 
            d['vocab']=vocab_serializer.data
            d['questions']=question_serializer.data
            d['topics']=topic_serializer.data
            d['skills']=skill_serializer.data

            return Response(d)
        except Book.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return HttpResponseServerError(ex)

    @action(methods=['GET'], detail=False)
    def books_by_current_profile(self, request):
        """Handle GET requests to profile resource

        Returns:
            Response -- JSON representation of user info
        """

        profile = Profile.objects.get(user=request.auth.user)

        # books =[]

        user_books = Book.objects.filter(profile_id = profile.id)
        all_user_books = Book.objects.filter(bookprofile__profile = profile)

        books = user_books | all_user_books

        searched_skill = self.request.query_params.get('skill', None)
        searched_topic = self.request.query_params.get('topic', None)
        searched_title = self.request.query_params.get('title', None)


        if searched_skill is not None:
            
            try:

                skill = Skill.objects.get(skill = searched_skill)
                books = books.filter(skills__skill = skill)


            except Book.DoesNotExist as ex:
                books = None
                return Response(books, status=status.HTTP_404_NOT_FOUND)
            except Exception:
                books = None
                return Response(books, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
        
        if searched_topic is not None:

            try:        
                topic = Topic.objects.get(topic = searched_topic)
                books = books.filter(topic__topic = topic)

            except Book.DoesNotExist as ex:
                books = None
                return Response(books, status=status.HTTP_404_NOT_FOUND)
            except Exception:
                books = None
                return Response(books, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        if searched_title is not None:
            try:
                def title_filter(book):
                    if searched_title in book.title:
                        return True
                    return False

                books = filter(title_filter, books)


            except Book.DoesNotExist as ex:
                books = None
                return Response(books, status=status.HTTP_404_NOT_FOUND)
            except Exception:
                books = None
                return Response(books, status=status.HTTP_500_INTERNAL_SERVER_ERROR)  
        
        for book in books:
            if book.profile_id == profile.id:
                book.is_current_user = True
            else:
                book.is_current_user = False

        books = BookSerializer(books, many=True, context={'request': request})

        return Response(books.data)

    @action(methods=['POST'], detail=True)
    def book_profile_rel(self, request, pk=None):

        book = Book.objects.get(pk=pk)
        profile = Profile.objects.get(user=request.auth.user)

        try:
            book_profile = BookProfile.objects.get(book=book, profile=profile)

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except BookProfile.DoesNotExist:

            # Creates a relationship object between the current book and the skill

            book_profile = BookProfile() 
            book_profile.book = book
            book_profile.profile = profile
            book_profile.save()

            return Response({}, status=status.HTTP_201_CREATED)

        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

class ProfileSerializer(serializers.ModelSerializer):
    """JSON serializer for topics

    Arguments:
        serializer type
    """ 

    class Meta:
        model = Profile
        fields = ('id', 'user') 


class VocabSerializer(serializers.ModelSerializer):
    """JSON serializer for topics

    Arguments:
        serializer type
    """ 

    class Meta:
        model = Vocab
        fields = ('id', 'word', 'page', 'definition', 'notes') 

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

class ProfileBookSerializer(serializers.ModelSerializer):
    """JSON serializer for books

    Arguments:
    serializer type
    """

    profile = ProfileSerializer(many=False)
 

    class Meta:
        model = Book
        fields = ('id', 'title', 'author', 'publish_year', 'notes', 'cover_url', 'rating', 'location', 'synopsis', 'profile', 'is_current_user')
        depth = 1


class BookSerializer(serializers.ModelSerializer):
    """JSON serializer for books

    Arguments:
        serializer type
    """

    class Meta:
        model = Book
        fields = ('id', 'title', 'author', 'publish_year', 'notes', 'cover_url', 'rating', 'location', 'synopsis', 'is_current_user')
        depth = 1

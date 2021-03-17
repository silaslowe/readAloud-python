"""View module for handling requests about games"""
from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rest_framework.decorators import action
from readAloudapi.models.vocab import Vocab
from readAloudapi.models.book import Book
from readAloudapi.models.book_vocab import BookVocab

class Vocabs(ViewSet):
    """Read Aloud vocab"""

    def create(self, request):

        """Handle POST operations

        Returns:
            Response -- JSON serialized vocab instance
        """

        book = Book.objects.get(pk=request.data['bookId'])

        vocab = Vocab()
        vocab.word = request.data['word']
        vocab.definition = request.data['definition']    
        vocab.page = request.data['page']
        vocab.notes = request.data['notes']



        # Try to save the new game to the database, then
        # serialize the game instance as JSON, and send the
        # JSON as a response to the client request

        try:
            vocab.save()
    
            # Create a book vocab relationship
            bookvocab = BookVocab()
            bookvocab.book = book
            bookvocab.vocab = vocab
            bookvocab.save()    

            serializer = VocabSerializer(vocab, context={'request': request})
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

        vocabs = Vocab.objects.all()

        word = self.request.query_params.get('word', None)

        if word is not None:
            def word_filter(vocab):
                if vocab.word == word:
                    return True
                return False
            
            vocabs = filter(word_filter, vocabs)


        serializer = VocabSerializer(vocabs, many=True, context={'request': request})
        return Response(serializer.data)

    @action(methods=['POST'], detail=False)
    def get_vocab_by_book(self, request):
        """Handle GET vocabs by book

        Returns:
            Response -- JSON serialized list of vocabs
        """

        book = Book.objects.get(pk=request.data["bookId"])
        vocabs = Vocab.objects.all().filter(bookvocab__book_id = book.id)

        serializer = VocabSerializer(vocabs, many=True, context={'request': request})

        return Response(serializer.data)

    def destroy(self, request, pk=None):
        try:
            vocab = Vocab.objects.get(pk=pk)
            vocab.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Vocab.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class VocabSerializer(serializers.ModelSerializer):
    """JSON serializer for vocab

    Arguments:
        serializer type
    """    

    class Meta:
        model = Vocab
        fields = ('id', 'word', 'definition', 'page', 'notes')
"""View module for handling requests about games"""
from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from readAloudapi.models import Book
from readAloudapi.models.profile import Profile
from django.contrib.auth.models import User


class Profiles(ViewSet):
    """Read Aloud Profiles"""

    def list(self, request):
        """Handle GET requests to profile resource

        Returns:
            Response -- JSON serialized list of profiles
        """        

        profiles = Profile.objects.all()

        serializer = ProfileSerializer(
            profiles, many=True, context={'request':request})
        return Response(serializer.data)



    # def update(self, request, pk=None):
    #     """Handle PUT requests for a profile

    #     Returns:
    #         Response -- Empty body with 204 status code
    #     """        

    #     # book = Book.objects.get(pk=request.data["bookId"])

    #     # Does mostly the same thing as POST, but instead of
    #     # creating a new instance of Profile, get the profile record
    #     # from the database whose primary key is `pk`

    #     user = User.objects.get(user=request.auth.user)


    #     profile = Profile.objects.get(pk=pk)




    #     class Profile(models.Model):
    #     user = models.OneToOneField(User, on_delete=models.CASCADE)
    #     role = models.CharField(max_length=25)
    #     bio = models.CharField(max_length=500)
    #     profile_pic = models.ImageField(upload_to='porfile_pics', height_field=None,width_field=None, max_length=None, null=True)


    #     #ORM for PUT method

    #     question.save()

    #     # 204 status code means everything worked but the
    #     # server is not sending back any data in the response

    #     return Response({}, status=status.HTTP_204_NO_CONTENT)
     

class UserSerializer(serializers.ModelSerializer):
    """JSON serializer for Users

    Arguments:
        serializer type
    """   

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name')

class ProfileSerializer(serializers.ModelSerializer):
    """JSON serializer for Profiles

    Arguments:
        serializer type
    """

    user = UserSerializer(many=False)

    class Meta:
        model = Profile
        fields =('id', 'user', 'bio', 'role', 'profile_pic')
        depth = 1
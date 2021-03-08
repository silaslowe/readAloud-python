from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields.files import ImageField

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=25)
    bio = models.CharField(max_length=500)
    profile_pic = models.ImageField(upload_to='porfile_pics', height_field=None,width_field=None, max_length=None, null=True)


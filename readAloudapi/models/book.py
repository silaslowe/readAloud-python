from django.db import models

class Book(models.Model):
    profile = models.ForeignKey("Profile", related_name="books", on_delete=models.CASCADE)
    title = models.CharField(max_length=75)
    author = models.CharField(max_length=75)
    publish_year = models.IntegerField()
    notes = models.TextField(max_length=1500)
    cover_url = models.CharField(max_length=125)
    rating = models.FloatField()
    location = models.CharField(max_length=50)
    synopsis = models.TextField(max_length=500)


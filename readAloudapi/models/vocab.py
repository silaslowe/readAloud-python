from django.db import models

class Vocab(models.Model):
    word = models.CharField(max_length=40)
    definition = models.CharField(max_length=255)
    page = models.CharField(max_length=3)
    notes = models.TextField(max_length=500)
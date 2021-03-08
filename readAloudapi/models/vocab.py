from django.db import models

class Vocab(models.Model):
    word = models.CharField(max_length=40)
    definition = models.CharField(max_length=255)
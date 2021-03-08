from django.db import models

class Topic(models.Model):
    topic = models.CharField(max_length=50)
    
from django.db import models

class Question(models.model):
    book = models.ForeignKey("Book", on_delete=models.CASCADE)
    question = models.CharField(max_length=150)
    page = models.CharField(max_length=3)
    
from django.db import models

class BookVocab(models.Model):
    book = models.ForeignKey("Book", on_delete=models.CASCADE)
    vocab = models.ForeignKey("Vocab", on_delete=models.CASCADE)

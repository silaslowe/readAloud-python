from django.db import models

class BookTopic(models.Model):
    book = models.ForeignKey("Book", on_delete=models.CASCADE)
    topic = models.ForeignKey("Topic", on_delete=models.CASCADE)
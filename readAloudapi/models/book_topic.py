from django.db import models

class BookTopic(models.Model):
    book = models.ForeignKey("Book", related_name="topic", on_delete=models.CASCADE)
    topic = models.ForeignKey("Topic", on_delete=models.CASCADE)
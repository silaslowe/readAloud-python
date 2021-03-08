from django.db import models

class Comment(models.Model):
    book = models.ForeignKey("Book", on_delete=models.CASCADE)
    profile = models.ForeignKey("Profile", on_delete=models.CASCADE)
    created_on = models.DateTimeField()
    comment = models.TextField(max_length=1000)

    
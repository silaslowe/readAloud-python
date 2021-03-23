from django.db import models

class BookProfile(models.Model):
    book = models.ForeignKey("Book", on_delete=models.CASCADE)
    profile = models.ForeignKey("Profile",  on_delete=models.CASCADE)
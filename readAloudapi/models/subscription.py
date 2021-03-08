from django.db import models

class Subscription(models.Model):
    profile = models.ForeignKey("Profile", on_delete=models.CASCADE)
    user = models.ForeignKey("User", on_delete=models.CASCADE)
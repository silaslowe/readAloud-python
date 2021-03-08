from django.db import models
from django.contrib.auth.models import User


class Subscription(models.Model):
    profile = models.ForeignKey("Profile", on_delete=models.CASCADE)
    user = models.ForeignKey("Profile", related_name="subscribee", on_delete=models.CASCADE)
from django.db import models

class BookSkill(models.Model):
    book = models.ForeignKey("Book", on_delete=models.CASCADE)
    skill = models.ForeignKey("Skill", on_delete=models.CASCADE)
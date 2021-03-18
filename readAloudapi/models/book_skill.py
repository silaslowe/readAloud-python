from django.db import models

class BookSkill(models.Model):
    book = models.ForeignKey("Book", related_name="skills", on_delete=models.CASCADE)
    skill = models.ForeignKey("Skill", related_name="books", on_delete=models.CASCADE)
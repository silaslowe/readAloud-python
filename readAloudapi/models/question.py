from django.db import models

class Question(models.Model):
    book = models.ForeignKey("Book", on_delete=models.CASCADE)
    question = models.CharField(max_length=150)
    page = models.CharField(max_length=3)
    
    @property
    def bookId(self):
        return self.__bookId

    @bookId.setter
    def bookId(self, value):
        self.__bookId = value
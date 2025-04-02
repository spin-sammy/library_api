from django.db import models
from django.core.validators import MinLengthValidator


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    published_date = models.DateField(null=True, blank=True)
    isbn = models.CharField(max_length=13, validators=[MinLengthValidator(13)], unique=True)
    pages = models.IntegerField(null=True, blank=True)
    cover = models.URLField(null=True, blank=True)
    language = models.CharField(max_length=50)

    def __str__(self):
        return self.title

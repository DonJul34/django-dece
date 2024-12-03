# models.py
from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=100)
    birth_year = models.IntegerField()

    def __str__(self):
        return self.name

class Publisher(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="books")  # One-to-Many
    publisher = models.OneToOneField(Publisher, on_delete=models.CASCADE)  # One-to-One
    publication_year = models.IntegerField()
    genres = models.ManyToManyField('Genre', related_name="books")  # Many-to-Many

    def __str__(self):
        return f"{self.title} by {self.author.name} ({self.publication_year})"

class Genre(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

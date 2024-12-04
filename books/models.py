# models.py
from django.db import models
from crm_app.models import Client  # Assuming the Client model is in crm_app
from django.conf import settings  # For referencing the User model
from client_library.models import Lecteur

class BookManager(models.Manager):
    def filter_books(self, user, title=None, author=None, year=None, genre=None, sort_by=None):
        """
        Filtre les livres associés à un utilisateur et/ou client en fonction des paramètres fournis.
        """
        books = self.filter(user=user)

        if title:
            books = books.filter(title__icontains=title)
        if author:
            books = books.filter(author__name__icontains=author)
        if year and year.isdigit():
            books = books.filter(publication_year__gte=int(year))
        if genre:
            books = books.filter(genres__name__icontains=genre)

        if sort_by in ['title', 'author__name', 'publication_year']:
            books = books.order_by(sort_by)

        return books


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
    author = models.ForeignKey('Author', on_delete=models.CASCADE, related_name="books")  # One-to-Many
    publisher = models.OneToOneField('Publisher', on_delete=models.CASCADE)  # One-to-One
    publication_year = models.IntegerField()
    genres = models.ManyToManyField('Genre', related_name="books")  # Many-to-Many
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="books")
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="books")
    lecteur = models.ForeignKey(
        'client_library.Lecteur',  # String reference to avoid circular import
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='books'
    )

    
    # Custom manager
    objects = BookManager()

    def __str__(self):
        return f"{self.title} by {self.author.name} ({self.publication_year})"
class Genre(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

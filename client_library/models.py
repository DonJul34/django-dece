from django.db import models
from crm_app.models import Client

class Lecteur(models.Model):
    name = models.CharField(max_length=100)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='lecteurs')

    def __str__(self):
        return self.name

class BorrowingHistory(models.Model):
    book = models.ForeignKey('books.Book', on_delete=models.CASCADE, related_name='history')  # String reference
    lecteur = models.ForeignKey(Lecteur, on_delete=models.SET_NULL, null=True)
    date_borrowed = models.DateTimeField(auto_now_add=True)
    date_returned = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.book.title} borrowed by {self.lecteur.name} on {self.date_borrowed}"

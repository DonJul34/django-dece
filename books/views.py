# views.py
from django.shortcuts import render
from .models import Book, Author, Genre
from django.contrib.auth.decorators import login_required

def book_list(request):
    # Récupération des filtres depuis l'URL
    title_query = request.GET.get('title', '')
    author_query = request.GET.get('author', '')
    year_query = request.GET.get('year', '')
    genre_query = request.GET.get('genre', '')
    sort_by = request.GET.get('sort_by', '')

    # Utilisation du manager pour appliquer les filtres
    books = Book.objects.filter_books(
        title=title_query,
        author=author_query,
        year=year_query,
        genre=genre_query,
        sort_by=sort_by
    )

    return render(request, 'books/book_list.html', {'books': books})
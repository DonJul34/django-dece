from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Book
from .forms import BookForm, AuthorForm, GenreForm
from rest_framework import viewsets
from .models import Author, Genre
from .serializers import AuthorSerializer, GenreSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.utils.translation import activate, get_language
from django.views import View

class SetLanguageView(View):
    def post(self, request, *args, **kwargs):
        language = request.POST.get('language')
        if language not in ['en', 'fr','es']:
            return JsonResponse({'error': 'Invalid language'}, status=400)

        activate(language)  # Set the active language
        request.session['django_language'] = language  # Save it to the session
        request.session.save()  # Ensure the session persists
        return JsonResponse({'message': 'Language updated successfully', 'language': language})
        
class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer

@login_required
def add_author(request):
    if request.method == "POST":
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('books:list')  # Redirect to book list after adding author
    else:
        form = AuthorForm()
    return render(request, 'books/add_author.html', {'form': form})

@login_required
def add_genre(request):
    if request.method == "POST":
        form = GenreForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('books:list')  # Redirect to book list after adding genre
    else:
        form = GenreForm()
    return render(request, 'books/add_genre.html', {'form': form})


@login_required
def book_create(request):
    """
    Create a new book and automatically create a new publisher.
    """
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save(commit=False)
            book.user = request.user
            # Retrieve the client associated with the logged-in user
            try:
                client = request.user.client  # Assuming OneToOne relation between User and Client
                book.client = client
            except Client.DoesNotExist:
                # Handle the case where the user does not have an associated client
                return render(request, 'books/error.html', {
                    'error_message': "No client associated with this user."
                })

            book.save()  # Save the book, along with the new publisher
            return redirect('books:list')  # Redirect to the book list after successful creation
    else:
        form = BookForm()

    return render(request, 'books/book_form.html', {'form': form})

@login_required
def book_list(request):
    """
    List all books associated with the logged-in user and apply filters/sorting.
    """
    # Get filter parameters from the request
    title_query = request.GET.get('title', '')
    author_query = request.GET.get('author', '')
    year_query = request.GET.get('year', '')
    genre_query = request.GET.get('genre', '')
    sort_by = request.GET.get('sort_by', '')

    try:
        # Use the custom manager to filter books for the logged-in user
        books = Book.objects.filter_books(
            user=request.user,
            title=title_query,
            author=author_query,
            year=year_query,
            genre=genre_query,
            sort_by=sort_by
        )
    except Exception as e:
        # Handle any potential issues and return an empty queryset
        books = Book.objects.none()

    return render(request, 'books/book_list.html', {'books': books})


@login_required
def book_delete(request, pk):
    """
    Delete a book associated with the logged-in user.
    """
    book = get_object_or_404(Book, pk=pk, user=request.user)
    if request.method == "POST":
        book.delete()
        return redirect('books:list')
    return render(request, 'books/book_confirm_delete.html', {'book': book})
# books/tests.py
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Author, Genre, Book
from .forms import AuthorForm, GenreForm, BookForm
import logging
import colorlog


handler = colorlog.StreamHandler()
handler.FileHandler("app.log")# Configure logger with colors

handler.setFormatter(colorlog.ColoredFormatter(
    "%(log_color)s%(levelname)s:%(name)s:%(message)s",
    log_colors={
        "DEBUG": "cyan",
        "INFO": "green",
        "WARNING": "yellow",
        "ERROR": "red",
        "CRITICAL": "bold_red",
    },
))
logger = logging.getLogger("books_tests")
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

class AuthorViewTests(TestCase):
    def setUp(self):
        logger.info("Setting up AuthorViewTests")
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')
        self.author = Author.objects.create(name="John Doe", birth_year=1970)

    def test_add_author_view_get(self):
        logger.info("Testing GET request for add_author view")
        response = self.client.get(reverse('books:add_author'))
        logger.debug(f"Response status code: {response.status_code}")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'books/add_author.html')

    def test_add_author_view_post_valid(self):
        logger.info("Testing POST request for add_author view with valid data")
        response = self.client.post(reverse('books:add_author'), {
            'name': 'Jane Smith',
            'birth_year': 1980
        })
        logger.debug(f"Response status code: {response.status_code}")
        self.assertEqual(response.status_code, 302)  # Redirect after success
        self.assertTrue(Author.objects.filter(name='Jane Smith').exists())

    def test_add_author_view_post_invalid(self):
        logger.info("Testing POST request for add_author view with invalid data")
        response = self.client.post(reverse('books:add_author'), {
            'name': '',  # Invalid: name is required
            'birth_year': 'invalid_year'
        })
        logger.debug(f"Response status code: {response.status_code}")
        self.assertEqual(response.status_code, 200)  # Re-render form with errors
        self.assertFormError(response, 'form', 'name', 'This field is required.')
        self.assertFormError(response, 'form', 'birth_year', 'Enter a whole number.')

class GenreViewTests(TestCase):
    def setUp(self):
        logger.info("Setting up GenreViewTests")
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')
        self.genre = Genre.objects.create(name="Fiction")

    def test_add_genre_view_get(self):
        logger.info("Testing GET request for add_genre view")
        response = self.client.get(reverse('books:add_genre'))
        logger.debug(f"Response status code: {response.status_code}")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'books/add_genre.html')

    def test_add_genre_view_post_valid(self):
        logger.info("Testing POST request for add_genre view with valid data")
        response = self.client.post(reverse('books:add_genre'), {
            'name': 'Non-Fiction'
        })
        logger.debug(f"Response status code: {response.status_code}")
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Genre.objects.filter(name='Non-Fiction').exists())

    def test_add_genre_view_post_invalid(self):
        logger.info("Testing POST request for add_genre view with invalid data")
        response = self.client.post(reverse('books:add_genre'), {
            'name': ''  # Invalid: name is required
        })
        logger.debug(f"Response status code: {response.status_code}")
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'name', 'This field is required.')

class BookViewTests(TestCase):
    def setUp(self):
        logger.info("Setting up all unit testing for Book management")
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')
        self.author = Author.objects.create(name="John Doe", birth_year=1970)
        self.genre = Genre.objects.create(name="Fiction")
        self.book = Book.objects.create(
            title="Sample Book",
            author=self.author,
            publication_year=2000,
            user=self.user,
            client=self.user.client  # Assuming user has an associated client
        )
        self.book.genres.add(self.genre)

    def test_book_create_view_get(self):
        logger.info("Testing GET request for validating that the view book_create exists and is linked to the template book_form.html (book_create view)")
        response = self.client.get(reverse('books:book_create'))
        logger.debug(f"Response status code: {response.status_code}")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'books/book_form.html')

    def test_book_create_view_post_valid(self):
        logger.info("Testing POST request for book_create view with valid data")
        response = self.client.post(reverse('books:book_create'), {
            'title': 'New Book',
            'author': self.author.id,
            'publication_year': 2021,
            'genres': [self.genre.id],
        })
        logger.debug(f"Response status code: {response.status_code}")
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Book.objects.filter(title='New Book').exists())

    def test_book_create_view_post_invalid(self):
        logger.info("Testing POST request for book_create view with invalid data")
        response = self.client.post(reverse('books:book_create'), {
            'title': '',  # Invalid: title is required
            'author': '',  # Invalid: author is required
            'publication_year': 'invalid_year',
        })
        logger.debug(f"Response status code: {response.status_code}")
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'title', 'This field is required.')
        self.assertFormError(response, 'form', 'author', 'This field is required.')
        self.assertFormError(response, 'form', 'publication_year', 'Enter a whole number.')

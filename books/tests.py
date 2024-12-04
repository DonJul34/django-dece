# books/tests.py
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from crm_app.models import Client  # Import Client from crm_app
from .models import Author, Genre, Book
from .forms import AuthorForm, GenreForm, BookForm
import logging
import colorlog

# Configure logger with colors for the console
stream_handler = colorlog.StreamHandler()
stream_handler.setFormatter(colorlog.ColoredFormatter(
    "%(log_color)s%(levelname)s:%(name)s:%(message)s",
    log_colors={
        "DEBUG": "cyan",
        "INFO": "green",
        "WARNING": "yellow",
        "ERROR": "red",
        "CRITICAL": "bold_red",
    },
))

# Configure FileHandler for logging to a file
file_handler = logging.FileHandler("books_tests.log")
file_formatter = logging.Formatter("%(asctime)s %(levelname)s:%(name)s:%(message)s")
file_handler.setFormatter(file_formatter)

# Set up the logger
logger = logging.getLogger("books_tests")
logger.addHandler(stream_handler)
logger.addHandler(file_handler)
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
        logger.info("Setting up BookViewTests")
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')
        
        # Create a Client instance for the user
        self.client_instance = Client.objects.create(
            user=self.user,
            name="Test Client",
            address="123 Test Street",
            phone="1234567890",
            email="testclient@example.com",
            industry="IT"
        )
        
        self.author = Author.objects.create(name="John Doe", birth_year=1970)
        self.genre = Genre.objects.create(name="Fiction")
        
        # If Publisher is required, create one
        # self.publisher = Publisher.objects.create(name="Test Publisher", country="USA")
        
        self.book = Book.objects.create(
            title="Sample Book",
            author=self.author,
            publication_year=2000,
            user=self.user,
            client=self.client_instance
            # publisher=self.publisher  # Uncomment if publisher is required
        )
        self.book.genres.add(self.genre)

    def test_book_create_view_get(self):
        logger.info("Testing GET request for book_create view")
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
            # 'publisher': self.publisher.id,  # Uncomment if publisher is required
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
            # 'publisher': '',  # Uncomment if publisher is required
        })
        logger.debug(f"Response status code: {response.status_code}")
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'title', 'This field is required.')
        self.assertFormError(response, 'form', 'author', 'This field is required.')
        self.assertFormError(response, 'form', 'publication_year', 'Enter a whole number.')

    def test_book_list_view(self):
        logger.info("Testing GET request for book_list view")
        response = self.client.get(reverse('books:list'))
        logger.debug(f"Response status code: {response.status_code}")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'books/book_list.html')
        self.assertContains(response, self.book.title)

    def test_book_delete_view_get(self):
        logger.info("Testing GET request for book_delete view")
        response = self.client.get(reverse('books:book_delete', args=[self.book.id]))
        logger.debug(f"Response status code: {response.status_code}")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'books/book_confirm_delete.html')

    def test_book_delete_view_post(self):
        logger.info("Testing POST request for book_delete view")
        response = self.client.post(reverse('books:book_delete', args=[self.book.id]))
        logger.debug(f"Response status code: {response.status_code}")
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Book.objects.filter(id=self.book.id).exists())

class BookManagerTests(TestCase):
    def setUp(self):
        logger.info("Setting up BookManagerTests")
        self.user = User.objects.create_user(username='manageruser', password='managerpass')
        self.client.login(username='manageruser', password='managerpass')
        
        # Create a Client instance for the user
        self.client_instance = Client.objects.create(
            user=self.user,
            name="Manager Client",
            address="456 Manager Street",
            phone="5555555555",
            email="manager@example.com",
            industry="Publishing"
        )
        
        self.author1 = Author.objects.create(name="Author One", birth_year=1980)
        self.author2 = Author.objects.create(name="Author Two", birth_year=1990)
        self.genre1 = Genre.objects.create(name="Fantasy")
        self.genre2 = Genre.objects.create(name="Science Fiction")

        self.book1 = Book.objects.create(
            title="Fantasy Book",
            author=self.author1,
            publication_year=2010,
            user=self.user,
            client=self.client_instance
        )
        self.book1.genres.add(self.genre1)

        self.book2 = Book.objects.create(
            title="Sci-Fi Book",
            author=self.author2,
            publication_year=2020,
            user=self.user,
            client=self.client_instance
        )
        self.book2.genres.add(self.genre2)

    def test_filter_books_by_title(self):
        logger.info("Testing filter_books with title filter")
        books = Book.objects.filter_books(user=self.user, title="Fantasy")
        self.assertIn(self.book1, books)
        self.assertNotIn(self.book2, books)

    def test_filter_books_by_author(self):
        logger.info("Testing filter_books with author filter")
        books = Book.objects.filter_books(user=self.user, author="Author Two")
        self.assertIn(self.book2, books)
        self.assertNotIn(self.book1, books)

    def test_filter_books_by_year(self):
        logger.info("Testing filter_books with publication_year filter")
        books = Book.objects.filter_books(user=self.user, year="2015")
        self.assertIn(self.book2, books)
        self.assertNotIn(self.book1, books)

    def test_filter_books_by_genre(self):
        logger.info("Testing filter_books with genre filter")
        books = Book.objects.filter_books(user=self.user, genre="Fantasy")
        self.assertIn(self.book1, books)
        self.assertNotIn(self.book2, books)

    def test_filter_books_with_sorting(self):
        logger.info("Testing filter_books with sorting")
        books = Book.objects.filter_books(user=self.user, sort_by='publication_year')
        self.assertEqual(list(books), [self.book1, self.book2])  # Assuming ascending order

    def test_filter_books_invalid_year(self):
        logger.info("Testing filter_books with invalid year filter")
        books = Book.objects.filter_books(user=self.user, year="invalid_year")
        # Should ignore the year filter
        self.assertIn(self.book1, books)
        self.assertIn(self.book2, books)

    def test_filter_books_no_filters(self):
        logger.info("Testing filter_books with no filters")
        books = Book.objects.filter_books(user=self.user)
        self.assertIn(self.book1, books)
        self.assertIn(self.book2, books)

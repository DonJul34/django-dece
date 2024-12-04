# crm_app/tests.py
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Client, Contact, Opportunity, Interaction
import logging
import colorlog

# Configure logger with colors
handler = colorlog.StreamHandler()
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
logger = logging.getLogger("crm_app_tests")
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

class ClientViewTests(TestCase):
    def setUp(self):
        logger.info("Setting up ClientViewTests")
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')
        self.client_instance = Client.objects.create(
            user=self.user,
            name="Test Client",
            address="123 Test Street",
            phone="123456789",
            email="testclient@example.com",
            industry="IT"
        )

    def test_signup_view_get(self):
        logger.info("Testing GET request for signup view")
        response = self.client.get(reverse('crm_app:signup'))
        logger.debug(f"Response status code: {response.status_code}")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'crm_app/signup.html')

    def test_signup_view_post_valid(self):
        logger.info("Testing POST request for signup view with valid data")
        response = self.client.post(reverse('crm_app:signup'), {
            'username': 'newuser',
            'password1': 'complexpassword123',
            'password2': 'complexpassword123',
            'name': 'New Client',
            'address': '456 New Avenue',
            'phone': '987654321',
            'email': 'newclient@example.com',
            'industry': 'Finance'
        })
        logger.debug(f"Response status code: {response.status_code}")
        self.assertEqual(response.status_code, 302)  # Redirect after successful signup
        self.assertTrue(User.objects.filter(username='newuser').exists())
        self.assertTrue(Client.objects.filter(email='newclient@example.com').exists())

    def test_signup_view_post_invalid(self):
        logger.info("Testing POST request for signup view with invalid data")
        response = self.client.post(reverse('crm_app:signup'), {
            'username': '',  # Invalid: username is required
            'password1': 'pass',
            'password2': 'pass',
            'name': '',
            'email': 'invalidemail',  # Invalid email format
            'industry': ''
        })
        logger.debug(f"Response status code: {response.status_code}")
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'username', 'This field is required.')
        self.assertFormError(response, 'form', 'name', 'This field is required.')
        self.assertFormError(response, 'form', 'email', 'Enter a valid email address.')
        self.assertFormError(response, 'form', 'industry', 'This field is required.')

class ContactViewTests(TestCase):
    def setUp(self):
        logger.info("Setting up ContactViewTests")
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')
        self.client_instance = Client.objects.create(
            user=self.user,
            name="Test Client",
            address="123 Test Street",
            phone="123456789",
            email="testclient@example.com",
            industry="IT"
        )
        self.contact = Contact.objects.create(
            first_name="John",
            last_name="Doe",
            phone="123456789",
            email="johndoe@example.com",
            position="Manager",
            client=self.client_instance
        )

    def test_add_contact_view_get(self):
        logger.info("Testing GET request for add_contact view")
        response = self.client.get(reverse('crm_app:add_contact'))
        logger.debug(f"Response status code: {response.status_code}")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'crm_app/add_contact.html')

    def test_add_contact_view_post_valid(self):
        logger.info("Testing POST request for add_contact view with valid data")
        response = self.client.post(reverse('crm_app:add_contact'), {
            'first_name': 'Jane',
            'last_name': 'Smith',
            'phone': '987654321',
            'email': 'janesmith@example.com',
            'position': 'Developer',
            'client': self.client_instance.id
        })
        logger.debug(f"Response status code: {response.status_code}")
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Contact.objects.filter(email='janesmith@example.com').exists())

    def test_add_contact_view_post_invalid(self):
        logger.info("Testing POST request for add_contact view with invalid data")
        response = self.client.post(reverse('crm_app:add_contact'), {
            'first_name': '',
            'last_name': '',
            'phone': 'invalid_phone',
            'email': 'invalidemail',
            'position': '',
            'client': ''
        })
        logger.debug(f"Response status code: {response.status_code}")
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'first_name', 'This field is required.')
        self.assertFormError(response, 'form', 'last_name', 'This field is required.')
        self.assertFormError(response, 'form', 'email', 'Enter a valid email address.')
        # Additional form errors can be checked similarly

# Additional test classes for Opportunity and Interaction can be added following the same pattern

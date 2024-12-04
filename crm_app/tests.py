# crm_app/tests.py
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Client, Contact, Opportunity, Interaction
from .forms import CustomUserCreationForm  # Ensure this form exists
import logging
import colorlog
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .serializers import ClientSerializer, ContactSerializer, OpportunitySerializer, InteractionSerializer
from books.models import Book  # Ensure this import is correct
from books.serializers import BookSerializer  # Ensure this serializer exists

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
file_handler = logging.FileHandler("crm_app_tests.log")
file_formatter = logging.Formatter("%(asctime)s %(levelname)s:%(name)s:%(message)s")
file_handler.setFormatter(file_formatter)

# Set up the logger
logger = logging.getLogger("crm_app_tests")
logger.addHandler(stream_handler)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)

# ---------------------------
# Model Tests
# ---------------------------
class ClientModelTests(TestCase):
    def setUp(self):
        logger.info("Setting up ClientModelTests")
        self.user = User.objects.create_user(username='clientuser', password='clientpass')
        self.client_instance = Client.objects.create(
            user=self.user,
            name="Test Client",
            address="123 Test Street",
            phone="123456789",
            email="testclient@example.com",
            industry="IT"
        )

    def test_client_creation(self):
        logger.info("Testing Client creation")
        self.assertEqual(self.client_instance.name, "Test Client")
        self.assertEqual(str(self.client_instance), "Test Client")

    def test_client_email_unique(self):
        logger.info("Testing unique email constraint for Client")
        with self.assertRaises(Exception):
            Client.objects.create(
                user=self.user,
                name="Another Client",
                address="456 Another Street",
                phone="987654321",
                email="testclient@example.com",  # Duplicate email
                industry="Finance"
            )

class ContactModelTests(TestCase):
    def setUp(self):
        logger.info("Setting up ContactModelTests")
        self.user = User.objects.create_user(username='contactuser', password='contactpass')
        self.client_instance = Client.objects.create(
            user=self.user,
            name="Contact Client",
            address="789 Contact Ave",
            phone="5555555555",
            email="contactclient@example.com",
            industry="Healthcare"
        )
        self.contact = Contact.objects.create(
            first_name="John",
            last_name="Doe",
            phone="1234567890",
            email="johndoe@example.com",
            position="Manager",
            client=self.client_instance
        )

    def test_contact_creation(self):
        logger.info("Testing Contact creation")
        self.assertEqual(str(self.contact), "John Doe")

class OpportunityModelTests(TestCase):
    def setUp(self):
        logger.info("Setting up OpportunityModelTests")
        self.user = User.objects.create_user(username='oppuser', password='opppass')
        self.client_instance = Client.objects.create(
            user=self.user,
            name="Opportunity Client",
            address="321 Opportunity Blvd",
            phone="4444444444",
            email="oppclient@example.com",
            industry="Retail"
        )
        self.opportunity = Opportunity.objects.create(
            title="New Opportunity",
            description="Opportunity Description",
            estimated_value=10000.00,
            status='new',
            client=self.client_instance
        )

    def test_opportunity_creation(self):
        logger.info("Testing Opportunity creation")
        self.assertEqual(str(self.opportunity), "New Opportunity")
        self.assertEqual(self.opportunity.status, 'new')

class InteractionModelTests(TestCase):
    def setUp(self):
        logger.info("Setting up InteractionModelTests")
        self.user = User.objects.create_user(username='intuser', password='intpass')
        self.client_instance = Client.objects.create(
            user=self.user,
            name="Interaction Client",
            address="654 Interaction Rd",
            phone="3333333333",
            email="intclient@example.com",
            industry="Manufacturing"
        )
        self.opportunity = Opportunity.objects.create(
            title="Interaction Opportunity",
            description="Interaction Opportunity Description",
            estimated_value=5000.00,
            status='in_progress',
            client=self.client_instance
        )
        self.interaction = Interaction.objects.create(
            date="2024-01-01",
            summary="First interaction summary.",
            opportunity=self.opportunity
        )

    def test_interaction_creation(self):
        logger.info("Testing Interaction creation")
        self.assertEqual(str(self.interaction), "Interaction on 2024-01-01 for Interaction Opportunity")

# ---------------------------
# View Tests
# ---------------------------
class SignupViewTests(TestCase):
    def setUp(self):
        logger.info("Setting up SignupViewTests")
        self.signup_url = reverse('crm_app:signup')  # Ensure this URL name matches your urls.py

    def test_signup_view_get(self):
        logger.info("Testing GET request for signup view")
        response = self.client.get(self.signup_url)
        logger.debug(f"Response status code: {response.status_code}")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'crm_app/signup.html')

    def test_signup_view_post_valid(self):
        logger.info("Testing POST request for signup view with valid data")
        response = self.client.post(self.signup_url, {
            'username': 'newuser',
            'password1': 'ComplexPass123',
            'password2': 'ComplexPass123',
            'name': 'New Client',
            'address': '456 New Avenue',
            'phone': '9876543210',
            'email': 'newclient@example.com',
            'industry': 'Finance'
        })
        logger.debug(f"Response status code: {response.status_code}")
        self.assertEqual(response.status_code, 302)  # Redirect after successful signup
        self.assertTrue(User.objects.filter(username='newuser').exists())
        self.assertTrue(Client.objects.filter(email='newclient@example.com').exists())

    def test_signup_view_post_invalid(self):
        logger.info("Testing POST request for signup view with invalid data")
        response = self.client.post(self.signup_url, {
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

class LoginViewTests(TestCase):
    def setUp(self):
        logger.info("Setting up LoginViewTests")
        self.user = User.objects.create_user(username='loginuser', password='loginpass')
        self.login_url = reverse('crm_app:login')  # Ensure this URL name matches your urls.py

    def test_login_view_get(self):
        logger.info("Testing GET request for login view")
        response = self.client.get(self.login_url)
        logger.debug(f"Response status code: {response.status_code}")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'crm_app/login.html')

    def test_login_view_post_valid(self):
        logger.info("Testing POST request for login view with valid credentials")
        response = self.client.post(self.login_url, {
            'username': 'loginuser',
            'password': 'loginpass'
        })
        logger.debug(f"Response status code: {response.status_code}")
        self.assertEqual(response.status_code, 302)  # Redirect after successful login
        self.assertTrue(response.url, reverse('books:list'))

    def test_login_view_post_invalid(self):
        logger.info("Testing POST request for login view with invalid credentials")
        response = self.client.post(self.login_url, {
            'username': 'loginuser',
            'password': 'wrongpass'
        })
        logger.debug(f"Response status code: {response.status_code}")
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', None, 'Please enter a correct username and password. Note that both fields may be case-sensitive.')

class AdminStatisticsViewTests(TestCase):
    def setUp(self):
        logger.info("Setting up AdminStatisticsViewTests")
        self.admin_user = User.objects.create_superuser(username='admin', password='adminpass')
        self.client.login(username='admin', password='adminpass')
        self.admin_statistics_url = reverse('admin_statistics')  # Ensure this URL name matches your urls.py

        # Create some clients
        Client.objects.create(
            user=User.objects.create_user(username='client1', password='pass1'),
            name="Client One",
            address="Address One",
            phone="1111111111",
            email="client1@example.com",
            industry="IT"
        )
        Client.objects.create(
            user=User.objects.create_user(username='client2', password='pass2'),
            name="Client Two",
            address="Address Two",
            phone="2222222222",
            email="client2@example.com",
            industry="Finance"
        )

    def test_admin_statistics_view_accessible_by_admin(self):
        logger.info("Testing admin_statistics view accessible by admin")
        response = self.client.get(self.admin_statistics_url)
        logger.debug(f"Response status code: {response.status_code}")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin/statistics_snippet.html')
        self.assertContains(response, "Total clients: 2")

    def test_admin_statistics_view_inaccessible_by_non_admin(self):
        logger.info("Testing admin_statistics view inaccessible by non-admin")
        self.client.logout()
        non_admin_user = User.objects.create_user(username='nonadmin', password='nonadminpass')
        self.client.login(username='nonadmin', password='nonadminpass')
        response = self.client.get(self.admin_statistics_url)
        logger.debug(f"Response status code: {response.status_code}")
        self.assertEqual(response.status_code, 403)  # Forbidden

# ---------------------------
# API ViewSet Tests
# ---------------------------
class ClientViewSetTests(APITestCase):
    def setUp(self):
        logger.info("Setting up ClientViewSetTests")
        self.client_user = User.objects.create_user(username='api_client_user', password='api_client_pass')
        self.client_instance = Client.objects.create(
            user=self.client_user,
            name="API Client",
            address="123 API Street",
            phone="3333333333",
            email="apiclient@example.com",
            industry="Tech"
        )
        self.api_client = APIClient()
        self.api_client.force_authenticate(user=self.client_user)
        self.client_viewset_url = reverse('client-list')  # Ensure this URL name matches your urls.py

    def test_get_clients_list(self):
        logger.info("Testing GET request for ClientViewSet list")
        response = self.api_client.get(self.client_viewset_url)
        clients = Client.objects.all()
        serializer = ClientSerializer(clients, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_client_via_api(self):
        logger.info("Testing POST request for ClientViewSet create via API")
        data = {
            'user': self.client_user.id,
            'name': 'API New Client',
            'address': '456 API Avenue',
            'phone': '4444444444',
            'email': 'apinnewclient@example.com',
            'industry': 'Healthcare'
        }
        response = self.api_client.post(self.client_viewset_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Client.objects.filter(email='apinnewclient@example.com').exists())

    def test_retrieve_client_detail(self):
        logger.info("Testing GET request for ClientViewSet retrieve")
        client_detail_url = reverse('client-detail', args=[self.client_instance.id])  # Ensure URL name
        response = self.api_client.get(client_detail_url)
        serializer = ClientSerializer(self.client_instance)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_update_client_via_api(self):
        logger.info("Testing PUT request for ClientViewSet update via API")
        client_detail_url = reverse('client-detail', args=[self.client_instance.id])
        data = {
            'user': self.client_user.id,
            'name': 'Updated API Client',
            'address': '789 Updated Street',
            'phone': '5555555555',
            'email': 'updatedapiclient@example.com',
            'industry': 'Finance'
        }
        response = self.api_client.put(client_detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client_instance.refresh_from_db()
        self.assertEqual(self.client_instance.name, 'Updated API Client')

    def test_delete_client_via_api(self):
        logger.info("Testing DELETE request for ClientViewSet via API")
        client_detail_url = reverse('client-detail', args=[self.client_instance.id])
        response = self.api_client.delete(client_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Client.objects.filter(id=self.client_instance.id).exists())

    def test_client_books_action(self):
        logger.info("Testing custom 'books' action in ClientViewSet")
        # Create a book linked to the client
        Book.objects.create(
            title="API Linked Book",
            author=None,  # Assuming Author is optional or create one if required
            publication_year=2023,
            user=self.client_user,
            client=self.client_instance
        )
        response = self.api_client.get(reverse('client-books'), {'user_id': self.client_user.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('books', response.data)
        self.assertEqual(len(response.data['books']), 1)
        self.assertEqual(response.data['books'][0]['title'], "API Linked Book")

    def test_create_client_via_action(self):
        logger.info("Testing custom 'create_client' action in ClientViewSet via API")
        response = self.api_client.get(reverse('client-create_client'), {
            'username': 'createduser',
            'password': 'createdpass',
            'name': 'Created Client',
            'address': '999 Created Ave',
            'phone': '6666666666',
            'email': 'createdclient@example.com',
            'industry': 'Education'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username='createduser').exists())
        self.assertTrue(Client.objects.filter(email='createdclient@example.com').exists())

    def test_delete_client_via_action(self):
        logger.info("Testing custom 'delete_client' action in ClientViewSet via API")
        response = self.api_client.get(reverse('client-delete_client'), {'user_id': self.client_user.id})
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Client.objects.filter(id=self.client_instance.id).exists())
        self.assertFalse(User.objects.filter(id=self.client_user.id).exists())

class ContactViewSetTests(APITestCase):
    def setUp(self):
        logger.info("Setting up ContactViewSetTests")
        self.user = User.objects.create_user(username='contactapiuser', password='contactapipass')
        self.client_instance = Client.objects.create(
            user=self.user,
            name="Contact API Client",
            address="123 Contact API Street",
            phone="7777777777",
            email="contactapi@example.com",
            industry="Logistics"
        )
        self.contact = Contact.objects.create(
            first_name="Alice",
            last_name="Smith",
            phone="8888888888",
            email="alice@example.com",
            position="Director",
            client=self.client_instance
        )
        self.api_client = APIClient()
        self.api_client.force_authenticate(user=self.user)
        self.contact_viewset_url = reverse('contact-list')  # Ensure this URL name matches your urls.py

    def test_get_contacts_list(self):
        logger.info("Testing GET request for ContactViewSet list")
        response = self.api_client.get(self.contact_viewset_url)
        contacts = Contact.objects.all()
        serializer = ContactSerializer(contacts, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_contact_via_api(self):
        logger.info("Testing POST request for ContactViewSet create via API")
        data = {
            'first_name': 'Bob',
            'last_name': 'Johnson',
            'phone': '9999999999',
            'email': 'bob@example.com',
            'position': 'Engineer',
            'client': self.client_instance.id
        }
        response = self.api_client.post(self.contact_viewset_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Contact.objects.filter(email='bob@example.com').exists())

    def test_retrieve_contact_detail(self):
        logger.info("Testing GET request for ContactViewSet retrieve")
        contact_detail_url = reverse('contact-detail', args=[self.contact.id])  # Ensure URL name
        response = self.api_client.get(contact_detail_url)
        serializer = ContactSerializer(self.contact)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_update_contact_via_api(self):
        logger.info("Testing PUT request for ContactViewSet update via API")
        contact_detail_url = reverse('contact-detail', args=[self.contact.id])
        data = {
            'first_name': 'Alice',
            'last_name': 'Brown',
            'phone': '1010101010',
            'email': 'alicebrown@example.com',
            'position': 'Senior Director',
            'client': self.client_instance.id
        }
        response = self.api_client.put(contact_detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.contact.refresh_from_db()
        self.assertEqual(self.contact.last_name, 'Brown')
        self.assertEqual(self.contact.email, 'alicebrown@example.com')

    def test_delete_contact_via_api(self):
        logger.info("Testing DELETE request for ContactViewSet via API")
        contact_detail_url = reverse('contact-detail', args=[self.contact.id])
        response = self.api_client.delete(contact_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Contact.objects.filter(id=self.contact.id).exists())

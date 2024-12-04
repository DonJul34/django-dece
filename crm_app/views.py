from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm  # Import your custom form
# Signup View
from django.db.models import Count
from .models import Client
from django.contrib.admin.views.decorators import staff_member_required
from rest_framework import viewsets
from .models import Client, Contact, Opportunity, Interaction
from .serializers import ClientSerializer, ContactSerializer, OpportunitySerializer, InteractionSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from books.models import Book  # Import du modèle Book
from books.serializers import BookSerializer  # Import du serializer Book

class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

    @action(detail=False, methods=['get'], url_path='books')
    def books(self, request):
        """
        Retrieve a client by user_id and include their associated books in the response.
        """
        user_id = request.query_params.get('user_id')
        if not user_id:
            return Response(
                {"error": "user_id parameter is required."},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            # Fetch the User and the linked Client
            user = User.objects.get(id=user_id)
            client = Client.objects.get(user=user)
        except User.DoesNotExist:
            return Response({"error": f"No user found with id {user_id}."}, status=status.HTTP_404_NOT_FOUND)
        except Client.DoesNotExist:
            return Response({"error": f"No client linked to user id {user_id}."}, status=status.HTTP_404_NOT_FOUND)

        # Retrieve all books linked to the client
        books = Book.objects.filter(client=client)

        # Serialize books and client
        books_serializer = BookSerializer(books, many=True)
        client_data = self.get_serializer(client).data
        client_data['books'] = books_serializer.data

        return Response(client_data, status=status.HTTP_200_OK)


    @action(detail=False, methods=['get'])
    def create_client(self, request):
        """
        Endpoint to create a client via URL parameters.
        If the User does not exist, it will be created.
        """
        # Retrieve parameters from the URL
        user_id = request.query_params.get('user_id')
        username = request.query_params.get('username', f"user_{user_id}")  # Fallback username
        password = request.query_params.get('password', 'defaultpassword')  # Default password for auto-created users
        name = request.query_params.get('name')
        address = request.query_params.get('address', '')
        phone = request.query_params.get('phone', '')
        email = request.query_params.get('email')
        industry = request.query_params.get('industry')

        # Validate required parameters
        if not (name and email and industry):
            return Response(
                {"error": "name, email, and industry are required."},
                status=status.HTTP_400_BAD_REQUEST
            )
        # Fetch or create the User
        user = None
        if user_id:
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                # Create a new User if user_id does not exist
                user = User.objects.create_user(username=username, password=password)
        else:
            # If no user_id is provided, create a new User
            if not username or not password:
                return Response(
                    {"error": "Either user_id or both username and password must be provided."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            user = User.objects.create_user(username=username, password=password)

        # Check if a client with the email already exists
        if Client.objects.filter(email=email).exists():
            return Response({"error": "A client with this email already exists."}, status=status.HTTP_400_BAD_REQUEST)

        # Create the client
        client = Client.objects.create(
            user=user,
            name=name,
            address=address,
            phone=phone,
            email=email,
            industry=industry
        )

        # Serialize and return the result
        serializer = self.get_serializer(client)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['get'])
    def delete_client(self, request):
        """
        Endpoint to delete a client using the user_id parameter.
        """
        user_id = request.query_params.get('user_id')

        if not user_id:
            return Response(
                {"error": "user_id parameter is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Fetch the user and associated client
            user = User.objects.get(id=user_id)
            client = Client.objects.get(user=user)
            client.delete()
            user.delete()  # Optionally delete the user as well
            return Response(
                {"message": f"Client with user_id {user_id} deleted successfully."},
                status=status.HTTP_204_NO_CONTENT
            )
        except User.DoesNotExist:
            return Response(
                {"error": f"No user found with user_id {user_id}."},
                status=status.HTTP_404_NOT_FOUND
            )
        except Client.DoesNotExist:
            return Response(
                {"error": f"No client found for user_id {user_id}."},
                status=status.HTTP_404_NOT_FOUND
            )
class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer

class OpportunityViewSet(viewsets.ModelViewSet):
    queryset = Opportunity.objects.all()
    serializer_class = OpportunitySerializer

class InteractionViewSet(viewsets.ModelViewSet):
    queryset = Interaction.objects.all()
    serializer_class = InteractionSerializer

@staff_member_required
def admin_statistics(request):
    """
    Génère des statistiques pour la page d'accueil de l'admin.
    """
    total_clients = Client.objects.count()

    # Récupération des statistiques d'industrie
    industries_stats = (
        Client.objects.values('industry')
        .annotate(count=Count('id'))
        .order_by('-count')
    )

    print(f"Total clients: {total_clients}")
    print(f"Industries stats: {industries_stats}")

    context = {
        'total_clients': total_clients,
        'industries_stats': industries_stats,
    }
    return render(request, 'admin/statistics_snippet.html', context)


def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # This saves both the User and Client
            login(request, user)
            return redirect('books:list')  # Redirect to books after signup
    else:
        form = CustomUserCreationForm()
    return render(request, 'crm_app/signup.html', {'form': form})
# Login View

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('books:list')  # Redirect to books after login
    else:
        form = AuthenticationForm()
    return render(request, 'crm_app/login.html', {'form': form})

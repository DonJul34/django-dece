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

class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

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

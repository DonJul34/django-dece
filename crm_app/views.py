from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm  # Import your custom form
# Signup View
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

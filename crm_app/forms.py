from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Client

class CustomUserCreationForm(UserCreationForm):
    # Add Client-specific fields
    name = forms.CharField(max_length=100, required=True, label="Client Name")
    address = forms.CharField(widget=forms.Textarea, required=True, label="Address")
    phone = forms.CharField(max_length=15, required=True, label="Phone")
    email = forms.EmailField(required=True, label="Email")
    industry = forms.CharField(max_length=100, required=True, label="Industry")

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'name', 'address', 'phone', 'email', 'industry']

    def save(self, commit=True):
        # Save the User instance first
        user = super().save(commit=False)

        if commit:
            user.save()

        # Create a Client instance linked to this User
        client = Client(
            name=self.cleaned_data['name'],
            address=self.cleaned_data['address'],
            phone=self.cleaned_data['phone'],
            email=self.cleaned_data['email'],
            industry=self.cleaned_data['industry']
        )
        if commit:
            client.save()

        return user

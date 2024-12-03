from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Client



class CustomUserCreationForm(UserCreationForm):
    """
    Formulaire personnalisé pour créer un utilisateur et un client associé.
    Génère automatiquement les champs à partir du modèle Client.
    """
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Dynamically add fields from the Client model
        client_form = forms.modelform_factory(
            Client,
            exclude=['id', 'user']  # Exclude fields like 'id' and 'user' that are handled programmatically
        )
        for name, field in client_form().fields.items():
            self.fields[name] = field

    def save(self, commit=True):
        # Save the User instance
        user = super().save(commit=False)

        if commit:
            user.save()

        # Create and link the Client instance to the User
        client = Client(
            user=user,  # Link the Client to the newly created User
            name=self.cleaned_data['name'],
            address=self.cleaned_data['address'],
            phone=self.cleaned_data['phone'],
            email=self.cleaned_data['email'],
            industry=self.cleaned_data['industry']
        )
        if commit:
            client.save()

        return user

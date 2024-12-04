from django import forms
from .models import Lecteur
from books.models import Book

class LecteurForm(forms.ModelForm):
    class Meta:
        model = Lecteur
        fields = ['name']

class ChangeLecteurForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['lecteur']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(ChangeLecteurForm, self).__init__(*args, **kwargs)
        try:
            client = user.client
            self.fields['lecteur'].queryset = Lecteur.objects.filter(client=client)
        except Client.DoesNotExist:
            self.fields['lecteur'].queryset = Lecteur.objects.none()

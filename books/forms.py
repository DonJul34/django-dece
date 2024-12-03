# forms.py
from django import forms
from .models import Book, Publisher, Author, Genre

class BookForm(forms.ModelForm):
    # Include publisher fields explicitly
    publisher_name = forms.CharField(max_length=100, label="Publisher Name")
    publisher_country = forms.CharField(max_length=50, label="Publisher Country")

    class Meta:
        model = Book
        exclude = ['id', 'user', 'client', 'publisher']  # Exclude fields set programmatically

    def save(self, commit=True):
        # Create a new publisher using the provided fields
        publisher = Publisher.objects.create(
            name=self.cleaned_data['publisher_name'],
            country=self.cleaned_data['publisher_country']
        )

        # Create the book instance but do not save it yet
        book = super().save(commit=False)
        book.publisher = publisher  # Associate the publisher with the book

        if commit:
            book.save()  # Save the book only after associating the publisher

        return book



class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['name', 'birth_year']

class GenreForm(forms.ModelForm):
    class Meta:
        model = Genre
        fields = ['name']
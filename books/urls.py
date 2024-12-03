# urls.py
from django.urls import path
from . import views
app_name = 'books'  # Ajoutez cette ligne pour enregistrer le namespace
urlpatterns = [
    path('', views.book_list, name='list'),  # URL name is 'list'
    ]

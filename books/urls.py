# urls.py
from django.urls import path
from . import views
app_name = 'books'  # Ajoutez cette ligne pour enregistrer le namespace

app_name = 'books'

urlpatterns = [
    path('', views.book_list, name='list'),
    path('create/', views.book_create, name='create'),
    path('create_author/', views.add_author, name='add_author'),
    path('create_genre/', views.add_genre, name='add_genre'),

    path('delete/<int:pk>/', views.book_delete, name='delete'),
]

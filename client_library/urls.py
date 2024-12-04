from django.urls import path
from . import views

app_name = 'client_library'

urlpatterns = [
    path('add/', views.add_lecteur, name='add_lecteur'),
    path('', views.lecteur_list, name='lecteur_list'),
    path('books/<int:book_id>/change_lecteur/', views.change_lecteur, name='change_lecteur'),
    path('books/<int:book_id>/history/', views.book_history, name='book_history'),
]

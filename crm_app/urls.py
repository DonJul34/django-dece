from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import ClientViewSet, ContactViewSet, OpportunityViewSet, InteractionViewSet,signup_view, login_view

# Créez un routeur et enregistrez vos ViewSets
app_name = 'crm_app'
urlpatterns = [
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
]

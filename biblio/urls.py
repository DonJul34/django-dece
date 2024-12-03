"""biblio URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from crm_app.views import ClientViewSet, ContactViewSet, OpportunityViewSet, InteractionViewSet

# Créez un routeur et enregistrez vos ViewSets
router = DefaultRouter()
router.register(r'clients', ClientViewSet)
router.register(r'contacts', ContactViewSet)
router.register(r'opportunities', OpportunityViewSet)
router.register(r'interactions', InteractionViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('books/', include('books.urls')),  # Books app
    path('', include('crm_app.urls')),  # CRM app
    path('api/', include(router.urls)),  # Incluez les routes de l'API
]

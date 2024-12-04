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
from books.views import AuthorViewSet, GenreViewSet
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# DOCUMENTATION API #
schema_view = get_schema_view(
   openapi.Info(
      title="API CRM",
      default_version='v1',
      description="Documentation de l'API CRM",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@crm.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

# ROUTE D'API #

router = DefaultRouter()

# ROUTE D'API POUR CRM APP#

router.register(r'clients', ClientViewSet)
router.register(r'contacts', ContactViewSet)
router.register(r'opportunities', OpportunityViewSet)

# ROUTE D'API POUR BOOKS APP#

router.register(r'author', AuthorViewSet)
router.register(r'genre', GenreViewSet)

# URL PATTERNS #

urlpatterns = [
    path('admin/', admin.site.urls),
    path('books/', include('books.urls')),  # Books app
    path('books/lecteurs/', include('client_library.urls')),  # Books app
    path('', include('crm_app.urls')),  # CRM app
    path('api/', include(router.urls)),  # Incluez les routes de l'API
    path('api/swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
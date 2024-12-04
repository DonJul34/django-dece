from django.apps import AppConfig


class ClientLibraryConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'client_library'
    
    def ready(self):
        import client_library.signals
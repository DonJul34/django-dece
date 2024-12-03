from django.apps import AppConfig

class BooksConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'books'
    
    def ready(self):
        # Importer les signaux ici pour éviter les importations circulaires
        import books.signals

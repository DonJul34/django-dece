from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import Book  # Assure-toi que seul Book est importé ici

@receiver(pre_save, sender=Book)
def before_saving_book(sender, instance, **kwargs):
    """
    Signal déclenché avant la sauvegarde d'un livre.
    """
    if instance.pk:
        print(f"Le livre '{instance.title}' (ID: {instance.pk}) est en cours de mise à jour.")
    else:
        print(f"Un nouveau livre '{instance.title}' est en cours de création.")

@receiver(post_save, sender=Book)
def after_saving_book(sender, instance, created, **kwargs):
    """
    Signal déclenché après la sauvegarde d'un livre.
    """
    if created:
        print(f"Un nouveau livre '{instance.title}' a été créé avec succès.")
        # Exemple : Notifier un administrateur ou mettre à jour un champ dépendant
    else:
        print(f"Le livre '{instance.title}' a été mis à jour.")
        # Exemple : Mettre à jour un index de recherche ou une relation dérivée

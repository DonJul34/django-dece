from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone
from books.models import Book
from .models import BorrowingHistory

@receiver(pre_save, sender=Book)
def track_lecteur_change(sender, instance, **kwargs):
    if instance.pk:
        try:
            previous = sender.objects.get(pk=instance.pk)
        except sender.DoesNotExist:
            return
        if previous.lecteur != instance.lecteur:
            # Close previous borrowing history
            last_history = BorrowingHistory.objects.filter(
                book=instance, date_returned__isnull=True
            ).last()
            if last_history:
                last_history.date_returned = timezone.now()
                last_history.save()
            # Create new borrowing history
            if instance.lecteur:
                BorrowingHistory.objects.create(book=instance, lecteur=instance.lecteur)

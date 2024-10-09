from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import PsychoProgress


@receiver(post_save, sender=PsychoProgress)
def send_email_on_completion(sender, instance, **kwargs):
    # Отправляем email только при завершении теста
    if instance.completed:
        instance.send_results_email()

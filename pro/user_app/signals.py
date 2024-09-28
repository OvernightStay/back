from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from .models import Player, Backpack
from pro.settings import DEFAULT_FROM_EMAIL


@receiver(post_save, sender=Player)
def massage_to_player(sender, instance, created, **kwargs):
    if created:
        # Создание содержимого письма на основе html шаблона
        context = {
            'login': instance.login,
            'password': instance.temporary_password,
            'first_name': instance.first_name,
            'last_name': instance.last_name,
            'email': instance.email,
        }
        html_content = render_to_string(
            template_name='email_sending/email_to_player.html',
            context=context,
        )

        # Создание письма клиенту
        player_message = EmailMultiAlternatives(
            subject='«Ночлежка»',
            body='',
            from_email=DEFAULT_FROM_EMAIL,
            to=[instance.email],
        )

        # Указание контента
        player_message.attach_alternative(html_content, 'text/html')

        # Отправка письма
        player_message.send()


# Автоматическое создание рюкзака при регистрации игрока
@receiver(post_save, sender=Player)
def create_player_backpack(sender, instance, created, **kwargs):
    if created and not instance.is_staff:
        Backpack.objects.create(player=instance)

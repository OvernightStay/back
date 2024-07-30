from django.core.mail import send_mail
from django.conf import settings


def send_verification_code_email(email, code):
    send_mail(
        '«Ночлежка»',
        f'Ваш код верификации игрового профиля в «Ночлежка»: {code}',
        settings.DEFAULT_FROM_EMAIL,
        [email],
        #fail_silently=False,
    )

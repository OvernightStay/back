from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.utils import timezone
from datetime import timedelta
import uuid


# Модель менеджера
class PlayerManager(BaseUserManager):
    def create_user(self, phone, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(phone=phone, email=email, **extra_fields)
        user.set_password(password)
        user.is_active = False  # Аккаунт неактивен до верификации по коду из письма
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(phone, email, password, **extra_fields)


# Данные игрока
class Player(AbstractUser, PermissionsMixin):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    
    objects = PlayerManager()
    
    phone = models.CharField(max_length=15, null=True, unique=True, verbose_name='Телефон')
    email = models.EmailField(max_length=50, null=True, unique=True)
    gender = models.CharField(max_length=1, null=True, choices=GENDER_CHOICES, verbose_name='Пол')
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания аккаунта')
    verification_code = models.CharField(max_length=6, blank=True, null=True, verbose_name='Код верификации')
    code_expiry = models.DateTimeField(blank=True, null=True, verbose_name='Срок действия кода')
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'phone']
    
    def generate_verification_code(self):
        code = str(uuid.uuid4().int)[:6]
        self.verification_code = code
        self.code_expiry = timezone.now() + timedelta(minutes=5)
        self.save()
        return code
    
    def __str__(self):
        return f'{self.first_name} {self.last_name} | {self.email}'

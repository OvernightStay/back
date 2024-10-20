from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta
import threading
import uuid


# Модель менеджера
class PlayerManager(BaseUserManager):
    def create_user(self, login, email=None, password=None, **extra_fields):
        if not login:
            raise ValueError("The Login field must be set")
        email = self.normalize_email(email) if email else None
        user = self.model(login=login, email=email, **extra_fields)
        user.set_password(password)

        if email:
            user.temporary_password = password
            user.temporary_password_created_at = timezone.now()

        user.save(using=self._db)

        if email:
            # Запуск таймера для очистки поля
            threading.Timer(10, self.clear_temporary_password, [user]).start()

        return user

    def clear_temporary_password(self, user):
        if (
            user.temporary_password
            and (timezone.now() - user.temporary_password_created_at).seconds >= 10
        ):
            user.temporary_password = None
            user.save()

    def create_superuser(self, login, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        user = self.create_user(login, email, password, **extra_fields)
        user.save(using=self._db)
        return user


# Данные игрока
class Player(AbstractUser, PermissionsMixin):
    GENDER_CHOICES = [
        ("M", "Male"),
        ("F", "Female"),
    ]

    objects = PlayerManager()

    username = models.CharField(
        max_length=50, null=True, blank=True, verbose_name="Имя пользователя"
    )
    login = models.CharField(max_length=50, unique=True, verbose_name="Логин")
    email = models.EmailField(max_length=50, null=True, blank=True, unique=True)
    phone = models.CharField(
        max_length=15, null=True, unique=True, verbose_name="Телефон"
    )
    gender = models.CharField(
        max_length=1, null=True, choices=GENDER_CHOICES, verbose_name="Пол"
    )
    training_check = models.BooleanField(default=False, verbose_name="Обучение")
    date_joined = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата создания аккаунта"
    )
    date_of_change = models.DateTimeField(
        auto_now=True, verbose_name="Дата изменения аккаунта"
    )
    verification_code = models.CharField(
        max_length=6, blank=True, null=True, verbose_name="Код верификации"
    )
    code_expiry = models.DateTimeField(
        blank=True, null=True, verbose_name="Срок действия кода"
    )
    temporary_password = models.CharField(
        max_length=128, null=True, blank=True, verbose_name="Временный пароль"
    )
    temporary_password_created_at = models.DateTimeField(
        null=True, blank=True, verbose_name="Время создания временного пароля"
    )

    USERNAME_FIELD = "login"
    REQUIRED_FIELDS = ["phone"]

    def generate_verification_code(self):
        code = str(uuid.uuid4().int)[:6]
        self.verification_code = code
        self.code_expiry = timezone.now() + timedelta(minutes=5)
        self.save()
        return code

    def __str__(self):
        return f"{self.first_name} {self.last_name} | {self.login} {self.phone}"

    class Meta:
        verbose_name = "Игрок"
        verbose_name_plural = "Игроки"


# Пример моделки для предметов в играх
class Item(models.Model):
    title = models.CharField(max_length=255, unique=True, verbose_name="Название")
    description = models.TextField(default="", verbose_name="Описание")
    image = models.ImageField(
        upload_to="images/", verbose_name="Изображение", null=True, blank=True
    )

    class Meta:
        verbose_name = "Предмет"
        verbose_name_plural = "Предметы"


# Менеджер для модели Рюкзака
class BackpackManager(models.Manager):
    # Переписывание метода создания для ограничения по количеству
    def create(self, *args, **kwargs):
        if self.model.objects.filter(player=kwargs["player"]).count() > 0:
            raise ValidationError("Достигнут лимит на создание обьектов")
        return super().create(*args, **kwargs)


# Рюкзак
class Backpack(models.Model):
    objects = BackpackManager()

    player = models.ForeignKey(Player, on_delete=models.CASCADE, verbose_name="Игрок")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")

    def __str__(self):
        return f"Backpack of {self.player.first_name} {self.player.last_name}"

    class Meta:
        verbose_name = "Рюкзак"
        verbose_name_plural = "Рюкзаки"


# Позиции рюкзака
class BackpackItem(models.Model):
    backpack = models.ForeignKey(
        Backpack, on_delete=models.CASCADE, verbose_name="Рюкзак"
    )
    item = models.ForeignKey(Item, on_delete=models.CASCADE, verbose_name="Предмет")

    class Meta:
        verbose_name = "Предмет рюкзака"
        verbose_name_plural = "Предметы рюкзака"

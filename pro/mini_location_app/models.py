from django.db import models
from user_app.models import Player
from django.utils import timezone
import uuid


class MiniNovella(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название новеллы')
    description = models.TextField(verbose_name='Описание новеллы')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Мини-новелла'
        verbose_name_plural = 'Мини-новеллы'


class MiniGame(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название игры')
    description = models.TextField(verbose_name='Описание игры')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Мини-игра'
        verbose_name_plural = 'Мини-игры'


class PlayerProgress(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='progress', verbose_name='Игрок')
    novella = models.ForeignKey(MiniNovella, on_delete=models.CASCADE, null=True, blank=True,
                                verbose_name='Мини-новелла')
    game = models.ForeignKey(MiniGame, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Мини-игра')
    completed = models.BooleanField(default=False, verbose_name='Завершено')
    experience_gained = models.IntegerField(default=0, verbose_name='Полученный опыт')
    reward = models.CharField(max_length=255, null=True, blank=True, verbose_name='Полученный подарок')
    completion_time = models.DateTimeField(default=timezone.now, verbose_name='Время завершения')

    def complete_progress(self):
        # Логика начисления опыта
        self.experience_gained = 100  # например, за каждую новеллу или игру 100 очков
        # Логика выдачи уникального подарка
        reward = Reward.objects.create(title='Уникальный подарок')
        self.reward = reward.title
        self.completed = True
        self.save()

    def __str__(self):
        return f'{self.player.login} | Новелла: {self.novella} | Игра: {self.game}'

    class Meta:
        verbose_name = 'Прогресс игрока'
        verbose_name_plural = 'Прогресс игроков'


class Reward(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название подарка')
    unique_code = models.UUIDField(default=uuid.uuid4, editable=False, unique=True,
                                   verbose_name='Уникальный код подарка')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Подарок'
        verbose_name_plural = 'Подарки'
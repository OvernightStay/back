from django.db import models
from user_app.models import Player
from django.utils import timezone
import uuid


class MiniNovella(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название новеллы')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Мини-новелла'
        verbose_name_plural = 'Мини-новеллы'


class MiniGame(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название игры')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Мини-игра'
        verbose_name_plural = 'Мини-игры'


class EmployeeGame(models.Model):
    title = models.CharField(max_length=100, verbose_name='Игра сотрудником')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Игра сотрудником'
        verbose_name_plural = 'Игра сотрудником'


class PlayerProgress(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='progress', verbose_name='Игрок')
    novella = models.ManyToManyField(MiniNovella, null=True, blank=True,
                                     verbose_name='Мини-новелла')
    game = models.ManyToManyField(MiniGame, null=True, blank=True, verbose_name='Мини-игра')
    employee = models.ManyToManyField(EmployeeGame, null=True, blank=True, verbose_name='Игра сотрудником')
    errors = models.PositiveIntegerField(default=0, verbose_name='Совершенные ошибки')
    experience_gained = models.PositiveIntegerField(default=0, verbose_name='Полученный опыт')
    reward = models.ManyToManyField('Reward', null=True, blank=True,
                                    verbose_name='Полученный подарок')
    completion_time = models.DateTimeField(default=timezone.now, verbose_name='Время завершения')

    def __str__(self):
        return f'{self.player.login} | Новелла: {self.novella} | Игра: {self.game}'

    class Meta:
        verbose_name = 'Прогресс игрока'
        verbose_name_plural = 'Прогресс игроков'


class Reward(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название подарка')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Подарок'
        verbose_name_plural = 'Подарки'

from django.db import models
from user_app.models import Player

from django.utils import timezone


class MiniNovella(models.Model):
    title = models.CharField(max_length=100, verbose_name="Название новеллы")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Мини-новелла"
        verbose_name_plural = "Мини-новеллы"


class MiniGame(models.Model):
    title = models.CharField(max_length=100, verbose_name="Название игры")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Мини-игра"
        verbose_name_plural = "Мини-игры"


class EmployeeGame(models.Model):
    title = models.CharField(max_length=100, verbose_name="Игра сотрудником")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Игра сотрудником"
        verbose_name_plural = "Игра сотрудником"


class Reward(models.Model):
    title = models.CharField(max_length=100, verbose_name="Название подарка")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Подарок"
        verbose_name_plural = "Подарки"


class PlayerProgress(models.Model):
    player = models.ForeignKey(
        Player, on_delete=models.CASCADE, related_name="progress", verbose_name="Игрок"
    )
    experience_gained = models.PositiveIntegerField(
        default=0, verbose_name="Полученный опыт"
    )
    completion_time = models.DateTimeField(
        default=timezone.now, verbose_name="Время завершения"
    )

    def __str__(self):
        return f"{self.player.login} | Прогресс игрока"

    class Meta:
        verbose_name = "Прогресс игрока"
        verbose_name_plural = "Прогресс игроков"


# Промежуточная модель для связи PlayerProgress и MiniNovella
class PlayerNovellaProgress(models.Model):
    player_progress = models.ForeignKey(
        PlayerProgress,
        on_delete=models.CASCADE,
        related_name="novella_progress",
        verbose_name="Прогресс игрока",
    )
    novella = models.ForeignKey(
        MiniNovella, on_delete=models.CASCADE, verbose_name="Мини-новелла"
    )

    class Meta:
        verbose_name = "Прогресс игрока по новелле"
        verbose_name_plural = "Прогресс игрока по новеллам"


# Промежуточная модель для связи PlayerProgress и MiniGame
class PlayerGameProgress(models.Model):
    player_progress = models.ForeignKey(
        PlayerProgress,
        on_delete=models.CASCADE,
        related_name="game_progress",
        verbose_name="Прогресс игрока",
    )
    game = models.ForeignKey(
        MiniGame, on_delete=models.CASCADE, verbose_name="Мини-игра"
    )

    class Meta:
        verbose_name = "Прогресс игрока по игре"
        verbose_name_plural = "Прогресс игрока по играм"


# Промежуточная модель для связи PlayerProgress и EmployeeGame
class PlayerEmployeeGameProgress(models.Model):
    player_progress = models.ForeignKey(
        PlayerProgress,
        on_delete=models.CASCADE,
        related_name="employee_game_progress",
        verbose_name="Прогресс игрока",
    )
    employee_game = models.ForeignKey(
        EmployeeGame, on_delete=models.CASCADE, verbose_name="Игра сотрудником"
    )

    class Meta:
        verbose_name = "Прогресс игрока по игре сотрудником"
        verbose_name_plural = "Прогресс игрока по играм сотрудниками"


# Промежуточная модель для связи PlayerProgress и Reward
class PlayerRewardProgress(models.Model):
    player_progress = models.ForeignKey(
        PlayerProgress,
        on_delete=models.CASCADE,
        related_name="reward_progress",
        verbose_name="Прогресс игрока",
    )
    reward = models.ForeignKey(Reward, on_delete=models.CASCADE, verbose_name="Подарок")

    class Meta:
        verbose_name = "Прогресс игрока по подаркам"
        verbose_name_plural = "Прогресс игрока по подаркам"

from django.db import models
from user_app.models import Player  # Импорт модели Player
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.db.models import ForeignKey
from .tasks import send_test_results_email
import asyncio


class Question(models.Model):
    text = models.CharField(max_length=255)
    question_number = models.PositiveIntegerField(unique=True, null=True, blank=True)  # Уникальный номер вопроса

    # def save(self, *args, **kwargs):
    #     if not self.question_number:  # Присваиваем номер только если он не задан
    #         last_question = Question.objects.order_by('question_number').last()
    #         if last_question:
    #             self.question_number = last_question.question_number + 1
    #         else:
    #             self.question_number = 1
    #     super(Question, self).save(*args, **kwargs)

    def __str__(self):
        return f"#{self.question_number}: {self.text}"


class Answer(models.Model):
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    number = models.PositiveIntegerField()  # Нумерация ответов (например, 1 и 2)

    def __str__(self):
        return f"{self.number}. {self.text}"


class TestProgress(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE, verbose_name='Игрок')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name='Вопрос')
    selected_answer = models.ForeignKey(Answer, on_delete=models.CASCADE, verbose_name='Выбранный ответ', null=True,
                                        blank=True)
    completed_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата прохождения')

    Player = Player()

    def save(self, *args, **kwargs):
        # Сохраняем объект
        super().save(*args, **kwargs)
        # Запускаем асинхронную задачу отправки почты
        asyncio.run(send_test_results_email(self.player, self.question, self.selected_answer))

    def __str__(self):
        return f'{self.player} - {self.question} - {self.selected_answer}'


class Meta:
    verbose_name = 'Прогресс теста'
    verbose_name_plural = 'Прогресс тестов'
    unique_together = ('player', 'question')  # Чтобы один игрок не мог ответить на один вопрос несколько раз

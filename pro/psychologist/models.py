from django.db import models
from user_app.models import Player  # Импорт модели Player


class Question(models.Model):
    text = models.CharField(max_length=255)
    question_number = models.PositiveIntegerField(unique=True)  # Убрано значение по умолчанию

    class Meta:
        ordering = ['question_number']
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'

    def __str__(self):
        return f"#{self.question_number}: {self.text}"


class Answer(models.Model):
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    number = models.PositiveIntegerField()  # Нумерация ответов (например, 1 и 2)

    class Meta:
        unique_together = ('question', 'number')
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'

    def __str__(self):
        return f"{self.number}. {self.text}"


class QuestionProgress(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE, verbose_name='Игрок')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name='Вопрос')
    selected_answer = models.ForeignKey(Answer, on_delete=models.SET_NULL, null=True, blank=True,
                                        verbose_name='Выбранный ответ')

    class Meta:
        verbose_name = 'Прогресс вопроса'
        verbose_name_plural = 'Прогресс вопросов'

    def __str__(self):
        return f"{self.player}: {self.question} - {self.selected_answer}"


class TestResult(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE, verbose_name='Игрок')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name='Вопрос')
    selected_answer = models.ForeignKey(Answer, null=True, blank=True, on_delete=models.SET_NULL,
                                        verbose_name='Выбранный ответ')
    completed_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата завершения')

    class Meta:
        verbose_name = 'Результат теста'
        verbose_name_plural = 'Результаты тестов'

    def __str__(self):
        return f"Игрок: {self.player}, Вопрос: {self.question}, Ответ: {self.selected_answer}"

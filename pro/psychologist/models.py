from django.db import models
from django.conf import settings


class Question(models.Model):
    text = models.CharField(max_length=255, verbose_name='Текст вопроса')
    next_question_if_first_answer = models.ForeignKey(
        'self', on_delete=models.SET_NULL, null=True, blank=True, related_name='first_answer_next_question',
        verbose_name='следующий вопрос, если первый ответ'
    )
    next_question_if_second_answer = models.ForeignKey(
        'self', on_delete=models.SET_NULL, null=True, blank=True, related_name='second_answer_next_question',
        verbose_name='следующий вопрос, если второй ответ'
    )

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers', verbose_name='Вопрос')
    text = models.CharField(max_length=255, verbose_name='Текст')
    is_first_option = models.BooleanField(default=True)  # для отслеживания, это первый или второй вариант

    def __str__(self):
        return f"Answer: {self.text} (Question: {self.question.text})"


    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'


class PsychoProgress(models.Model):
    player = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='psychologist_progress')
    current_question = models.ForeignKey(Question, on_delete=models.SET_NULL, null=True, blank=True)
    selected_answers = models.ManyToManyField(Answer, blank=True, related_name='player_answers')
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"Progress of {self.player.login} | Current Question: {self.current_question.text if self.current_question else 'None'}"

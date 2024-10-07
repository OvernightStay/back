from django.db import models
from django.conf import settings


class Question(models.Model):
    text = models.CharField(max_length=255)
    next_question_if_first_answer = models.ForeignKey(
        'self', on_delete=models.SET_NULL, null=True, blank=True, related_name='first_answer_next_question'
    )
    next_question_if_second_answer = models.ForeignKey(
        'self', on_delete=models.SET_NULL, null=True, blank=True, related_name='second_answer_next_question'
    )

    def __str__(self):
        return self.text


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    text = models.CharField(max_length=255)
    is_first_option = models.BooleanField(default=True)  # для отслеживания, это первый или второй вариант

    def __str__(self):
        return f"Answer: {self.text} (Question: {self.question.text})"


class PsychoProgress(models.Model):
    player = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='psychologist_progress')
    current_question = models.ForeignKey(Question, on_delete=models.SET_NULL, null=True, blank=True)
    selected_answers = models.ManyToManyField(Answer, blank=True, related_name='player_answers')
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"Progress of {self.player.login} | Current Question: {self.current_question.text if self.current_question else 'None'}"

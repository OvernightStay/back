from django.db import models

from user_app.models import Player  # Импорт модели Player


class Question(models.Model):
    text = models.CharField(max_length=255)
    answer_type = models.CharField(max_length=50,
                                   choices=[('single', 'Single Choice'), ('multiple', 'Multiple Choice')])
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="questions")  # Связь с игроком

    def __str__(self):
        return self.text


class Answer(models.Model):
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    next_question = models.ForeignKey(Question, null=True, blank=True, related_name='next_questions',
                                      on_delete=models.SET_NULL)

    def __str__(self):
        return self.text


class PlayerTestResult(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="test_results")
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    completed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Player: {self.player.login} | Question: {self.question.text} | Answer: {self.answer.text}"

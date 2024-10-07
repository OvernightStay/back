from django.db import models


class Question(models.Model):
    text = models.CharField(max_length=255)

    def __str__(self):
        return self.text


class Answer(models.Model):
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    next_question = models.ForeignKey(Question, related_name='next_answers', null=True, blank=True,
                                      on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.text} (Next: {self.next_question})"

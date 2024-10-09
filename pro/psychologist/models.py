from django.db import models
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


# Модель вопроса
class Question(models.Model):
    text = models.CharField(max_length=255, verbose_name="Текст вопроса")

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"


# Модель ответа
class Answer(models.Model):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name="answers",
        verbose_name="Вопрос",
    )
    text = models.CharField(max_length=255, verbose_name="Текст ответа")
    order = models.PositiveIntegerField(verbose_name="Порядок ответа", default=1)

    def __str__(self):
        # Здесь мы указываем, что в строковом представлении выводим текст ответа и вопроса
        return f"Answer: {self.text} (Question: {self.question.text})"

    class Meta:
        verbose_name = "Ответ"
        verbose_name_plural = "Ответы"
        unique_together = ("question", "order")  # Уникальность по вопросу и порядку


# Модель перехода между вопросами на основе выбранного ответа
class QuestionTransition(models.Model):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name="transitions",
        verbose_name="Вопрос",
    )
    answer = models.ForeignKey(
        Answer,
        on_delete=models.CASCADE,
        related_name="next_question_transition",
        verbose_name="Ответ",
    )
    next_question = models.ForeignKey(
        Question,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="previous_questions",
        verbose_name="Следующий вопрос",
    )

    def __str__(self):
        return f"Transition: {self.question.text} -> {self.next_question.text if self.next_question else 'None'} via {self.answer.text}"

    class Meta:
        verbose_name = "Переход между вопросами"
        verbose_name_plural = "Переходы между вопросами"


# Модель прогресса игрока
class PsychoProgress(models.Model):
    player = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="player_psy_progress",
        verbose_name="Игрок",
    )
    current_question = models.ForeignKey(
        Question,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Текущий вопрос",
    )
    selected_answers = models.ManyToManyField(
        Answer,
        blank=True,
        related_name="player_answers",
        verbose_name="Выбранные ответы",
    )
    completed = models.BooleanField(default=False, verbose_name="Завершен")
    asked_questions = models.ManyToManyField(
        Question,
        blank=True,
        related_name="asked_by_players",
        verbose_name="Заданные вопросы",
    )

    def __str__(self):
        return f"Progress of {self.player.username} | Current Question: {self.current_question.text if self.current_question else 'None'}"

    def next_question(self, answer):
        transition = QuestionTransition.objects.filter(
            question=self.current_question, answer=answer
        ).first()

        if transition and transition.next_question:
            self.current_question = transition.next_question
            self.save()
        else:
            self.completed = True
            self.save()

    def send_results_email(self):
        """
        Отправляет результаты на почту игроку после завершения теста
        """
        context = {
            "player": self.player,
            "answers": self.selected_answers.all(),
        }

        # Генерация HTML-контента письма на основе шаблона
        html_content = render_to_string(
            "email_sending/psychologist_test_results.html", context
        )

        # Создание письма с HTML-контентом
        subject = "Результаты вашего психологического теста"
        from_email = settings.DEFAULT_FROM_EMAIL
        to_email = [self.player.email]

        email = EmailMultiAlternatives(
            subject=subject,
            body="Результаты теста прилагаются ниже.",
            from_email=from_email,
            to=to_email,
        )

        # Добавление HTML-контента
        email.attach_alternative(html_content, "text/html")

        # Отправка письма
        email.send()

    class Meta:
        verbose_name = "Прогресс игрока"
        verbose_name_plural = "Прогрессы игроков"
        constraints = [
            models.UniqueConstraint(
                fields=["player"],
                condition=models.Q(completed=False),
                name="unique_active_progress",
            )
        ]

from django.core.mail import send_mail
from django.conf import settings
from .models import QuestionProgress, TestResult


def save_test_results(player):
    # Получаем все прогрессы вопросов для игрока
    question_progresses = QuestionProgress.objects.filter(player=player)

    # Сохраняем каждый результат в модель TestResult
    for progress in question_progresses:
        TestResult.objects.create(
            player=player,
            question=progress.question,
            selected_answer=progress.selected_answer
        )


def send_test_results(player):
    # Получаем все прогрессы вопросов для игрока
    question_progresses = QuestionProgress.objects.filter(player=player)

    # Формируем текст письма
    email_content = f"Результаты теста игрока {player}:\n\n"
    for progress in question_progresses:
        email_content += f"Вопрос: {progress.question.text}\n"
        email_content += f"Выбранный ответ: {progress.selected_answer.text if progress.selected_answer else 'Ответ не выбран'}\n\n"

    # Отправляем письмо администратору
    send_mail(
        subject=f"Результаты теста игрока {player}",
        message=email_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[settings.ADMIN_EMAIL],
        fail_silently=False,
    )

    # Сохраняем результаты в базу данных
    save_test_results(player)

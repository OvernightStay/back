# tasks.py
import asyncio
from django.core.mail import send_mail
from django.conf import settings


async def send_test_results_email(player, question, selected_answer):
    subject = 'Test Completion Notification'
    message = (
        f'Player: {player.login}\n'
        f'Question: {question.text}\n'
        f'Selected Answer: {selected_answer.text}\n'
    )
    recipient_list = [settings.DEFAULT_FROM_EMAIL]  # Email администратора
    await asyncio.to_thread(send_mail, subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)

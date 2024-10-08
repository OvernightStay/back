from django.contrib import admin
from .models import Question, Answer, PlayerTestResult


# Inline модель для вариантов ответов
class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 2  # Количество пустых полей для ответов при создании нового вопроса
    fields = ('text', 'next_question')  # Поля, которые будут отображаться
    fk_name = 'question'  # Указываем конкретное поле ForeignKey

# Регистрация модели вопроса с inline-ответами
@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'answer_type')  # Отображаем текст вопроса и тип ответа
    inlines = [AnswerInline]  # Добавляем inline-модель для ответов


# Регистрация модели ответов (если нужно отдельно редактировать)
@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('text', 'question', 'next_question')  # Поля, которые будут отображаться в списке ответов


@admin.register(PlayerTestResult)
class PlayerTestResultAdmin(admin.ModelAdmin):
    list_display = ('player', 'question', 'answer', 'completed_at')

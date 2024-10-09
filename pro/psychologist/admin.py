from django.contrib import admin
from .models import Question, Answer, QuestionTransition, PsychoProgress


# Настройка админки для модели Question
class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 1  # Количество дополнительных ответов, которые будут отображаться


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'text')  # Поля, которые будут отображаться в списке вопросов
    search_fields = ('text',)  # Поля, по которым можно будет искать
    inlines = [AnswerInline]  # Вложенные ответы в интерфейсе редактирования вопроса


# Настройка админки для модели Answer
@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'question', 'text', 'order')  # Поля, которые будут отображаться в списке ответов
    list_filter = ('question',)  # Фильтрация по вопросам
    search_fields = ('text',)  # Поля, по которым можно будет искать


# Настройка админки для модели QuestionTransition
@admin.register(QuestionTransition)
class QuestionTransitionAdmin(admin.ModelAdmin):
    list_display = ('id', 'question', 'answer', 'next_question')  # Поля, которые будут отображаться в списке переходов
    list_filter = ('question',)  # Фильтрация по вопросам
    search_fields = ('question__text', 'answer__text', 'next_question__text')  # Поиск по текстам вопросов и ответов


# Настройка админки для модели PsychoProgress
@admin.register(PsychoProgress)
class PsychoProgressAdmin(admin.ModelAdmin):
    list_display = (
    'id', 'player', 'current_question', 'completed')  # Поля, которые будут отображаться в списке прогресса
    list_filter = ('player', 'completed')  # Фильтрация по игрокам и завершенности
    search_fields = ('player__username',)  # Поиск по имени пользователя игрока

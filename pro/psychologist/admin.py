from django.contrib import admin
from .models import Question, Answer, QuestionProgress, TestResult


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 2  # Количество пустых полей для ввода ответов


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_number', 'text')  # Поля для отображения в списке вопросов
    search_fields = ('text',)  # Возможность поиска по тексту вопроса
    ordering = ('question_number',)  # Сортировка по номеру вопроса
    inlines = [AnswerInline]  # Возможность добавления ответов прямо в форме вопроса


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('question', 'number', 'text')  # Поля для отображения в списке ответов
    list_filter = ('question',)  # Фильтр по вопросу
    search_fields = ('text',)  # Поиск по тексту ответа


@admin.register(QuestionProgress)
class QuestionProgressAdmin(admin.ModelAdmin):
    list_display = ('player', 'question', 'selected_answer')  # Поля для отображения в списке прогресса
    list_filter = ('player', 'question')  # Фильтры по игроку и вопросу
    search_fields = ('player__username', 'question__text')  # Поиск по игроку и тексту вопроса


@admin.register(TestResult)
class TestResultAdmin(admin.ModelAdmin):
    list_display = ('player', 'question', 'selected_answer', 'completed_at')
    list_filter = ('player', 'completed_at')
    search_fields = ('player__username', 'question__text')

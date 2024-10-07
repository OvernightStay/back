from django.contrib import admin
from .models import Question, Answer, PsychoProgress


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 2  # Позволяет добавлять сразу два варианта ответа
    fields = ['text', 'is_first_option']


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['text', 'next_question_if_first_answer', 'next_question_if_second_answer']
    inlines = [AnswerInline]  # Добавляем вариант ответа как инлайн
    search_fields = ['text']
    list_filter = ['next_question_if_first_answer', 'next_question_if_second_answer']


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['text', 'question', 'is_first_option']
    list_filter = ['is_first_option', 'question']
    search_fields = ['text', 'question__text']


@admin.register(PsychoProgress)
class PlayerProgressAdmin(admin.ModelAdmin):
    list_display = ['player', 'current_question', 'completed']
    list_filter = ['completed', 'player']
    search_fields = ['player__login', 'current_question__text']
    filter_horizontal = ['selected_answers']

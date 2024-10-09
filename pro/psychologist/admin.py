from django.contrib import admin
from .models import Question, Answer, QuestionTransition, PsychoProgress


# Настройка админки для модели Question
class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 1


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("id", "text")
    search_fields = ("text",)
    inlines = [AnswerInline]


# Настройка админки для модели Answer
@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ("id", "question", "text", "order")
    list_filter = ("question",)
    search_fields = ("text",)


# Настройка админки для модели QuestionTransition
@admin.register(QuestionTransition)
class QuestionTransitionAdmin(admin.ModelAdmin):
    list_display = ("id", "question", "answer", "next_question")
    list_filter = ("question",)
    search_fields = ("question__text", "answer__text", "next_question__text")


# Настройка админки для модели PsychoProgress
@admin.register(PsychoProgress)
class PsychoProgressAdmin(admin.ModelAdmin):
    list_display = ("id", "player", "current_question", "completed")
    list_filter = ("player", "completed")
    search_fields = ("player__username",)

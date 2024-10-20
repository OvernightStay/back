from django.contrib import admin
from .models import Question, Answer, QuestionProgress


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 2


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("question_number", "text")
    list_filter = ("question_number",)
    search_fields = ("text",)
    inlines = [AnswerInline]


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ("question", "number", "text")
    list_filter = ("question",)
    search_fields = ("text",)


@admin.register(QuestionProgress)
class QuestionProgressAdmin(admin.ModelAdmin):
    list_display = ("player", "question", "selected_answer")
    list_filter = ("player", "question")
    search_fields = ("player__username", "question__text")

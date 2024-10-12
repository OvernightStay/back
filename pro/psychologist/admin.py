import csv
from django.http import HttpResponse
from django.contrib import admin
from .models import Question, Answer, TestProgress


# Инлайн-редактирование ответов внутри вопросов
class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 2  # Количество пустых строк для добавления новых ответов
    min_num = 2  # Минимум 2 ответа для каждого вопроса
    max_num = 2  # Максимум 2 ответа для каждого вопроса
    fields = ['number', 'text']  # Поля для отображенxия


# Функция экспорта в CSV
def export_to_csv(modeladmin, request, queryset):
    # Определяем заголовки для CSV файла
    meta = modeladmin.model._meta
    field_names = [field.name for field in meta.fields]

    # Создаем HTTP-ответ с указанием заголовка для скачивания файла
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename={meta}.csv'

    # Пишем данные в CSV-файл
    writer = csv.writer(response)
    writer.writerow(field_names)  # Записываем заголовки столбцов

    # Записываем строки данных
    for obj in queryset:
        writer.writerow([getattr(obj, field) for field in field_names])

    return response


# Название и описание экшена для админки
export_to_csv.short_description = 'Export to CSV'


# Админка для вопросов
@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_number', 'text')  # Поля для отображения в списке
    search_fields = ('text',)  # Поле для поиска
    inlines = [AnswerInline]  # Включаем инлайн-редактирование ответов
    ordering = ['question_number']  # Упорядочивание по номеру вопроса
    # readonly_fields = ['question_number']  # Номер вопроса присваивается автоматически

    # Добавляем action для экспорта
    actions = [export_to_csv]


# Админка для прогресса тестов
@admin.register(TestProgress)
class TestProgressAdmin(admin.ModelAdmin):
    list_display = ('player', 'question', 'selected_answer', 'completed_at')  # Поля для отображения
    list_filter = ('player', 'completed_at')  # Фильтры для игроков и даты прохождения
    search_fields = ('player__login', 'question__text')  # Поля для поиска по логину игрока и тексту вопроса
    autocomplete_fields = ['player', 'question',
                           'selected_answer']  # Автозаполнение при выборе игрока, вопроса и ответа
    ordering = ['-completed_at']  # Сортировка по дате прохождения

    # Добавляем action для экспорта
    actions = [export_to_csv]


# Регистрация модели Answer в админ-панели
@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('number', 'text', 'question')  # Отображаемые поля в списке объектов
    list_filter = ('question',)  # Фильтры в правой панели
    search_fields = ('text', 'question__text')  # Поля для поиска
    ordering = ('number',)  # Сортировка по умолчанию

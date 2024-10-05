from django.contrib import admin
from .models import Book

# Регистрация модели Book в админ-панели
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'date_add', 'date_update')  # Поля, которые будут отображаться в списке объектов
    list_filter = ('date_add', 'date_update')  # Фильтры в правой боковой панели
    search_fields = ('title', 'text')  # Поля, по которым можно осуществлять поиск
    prepopulated_fields = {'slug': ('title',)}  # Автоматическое заполнение поля slug на основе поля title
    readonly_fields = ('date_add', 'date_update')  # Поля, которые будут доступны только для чтения

    fieldsets = (
        (None, {
            'fields': ('title', 'text', 'slug', 'image_start', 'image_end')
        }),
        ('Даты', {
            'fields': ('date_add', 'date_update'),
            'classes': ('collapse',),
        }),
    )
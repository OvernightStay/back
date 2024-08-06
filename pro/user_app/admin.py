from django.contrib import admin

from .models import Player


# Регистрируем модели в админке
@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = (
        'first_name', 'last_name', 'training_check', 'login', 'email', 'phone', 'gender', 'date_joined',
        'date_of_change')
    search_fields = ('login', 'email', 'phone', 'last_name')
    list_filter = ('gender', 'is_staff', 'is_active')
    ordering = ('-date_joined',)
    list_display_links = ('first_name', 'last_name', 'login',)
    readonly_fields = ('date_joined', 'training_check', 'date_of_change')
    list_per_page = 10
    fieldsets = (
        (None, {
            'fields': ('first_name', 'last_name', 'training_check', 'login', 'email', 'phone', 'gender', 'date_joined')
        }),
    )

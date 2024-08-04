from django.contrib import admin
from .models import Player


class PlayerAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'login', 'email', 'phone', 'gender', 'date_joined')
    search_fields = ('login', 'email', 'phone', 'last_name')
    list_filter = ('gender', 'is_staff', 'is_active')
    ordering = ('date_joined',)


# Регистрируем модели в админке
admin.site.register(Player, PlayerAdmin)

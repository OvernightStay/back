from django.contrib import admin
from .models import Player


class PlayerAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'phone', 'email', 'gender', 'date_joined')
    search_fields = ('last_name', 'phone', 'email')
    list_filter = ('gender', 'date_joined', 'is_staff', 'is_active')
    ordering = ('date_joined',)


# Регистрируем модели в админке
admin.site.register(Player, PlayerAdmin)

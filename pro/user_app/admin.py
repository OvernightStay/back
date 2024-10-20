from django.contrib import admin

from .models import Player


# Регистрируем модели в админке
@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = (
        "last_name",
        "first_name",
        "login",
        "email",
        "phone",
        "gender",
        "training_check",
        "date_joined",
        "date_of_change",
    )
    search_fields = (
        "login",
        "email",
        "phone",
        "last_name",
        "first_name",
    )
    list_filter = ("gender", "is_staff", "is_active")
    ordering = ("-date_joined",)
    list_display_links = (
        "first_name",
        "last_name",
        "login",
    )
    readonly_fields = (
        "date_joined",
        "training_check",
        "date_of_change",
        "is_staff",
        "is_active",
    )
    list_per_page = 10
    fieldsets = (
        (
            "Личные данные",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "login",
                    "gender",
                )
            },
        ),
        (
            "Контактная информация",
            {
                "fields": (
                    "email",
                    "phone",
                )
            },
        ),
        (
            "Дополнительная информация",
            {
                "description": "Указанная информация изменяется автоматически",
                "fields": (
                    "training_check",
                    "is_staff",
                    "is_active",
                    "date_joined",
                    "date_of_change",
                ),
            },
        ),
    )

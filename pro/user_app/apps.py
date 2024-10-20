from django.apps import AppConfig


class UserAppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "user_app"
    verbose_name = "Управление пользователями"

    def ready(self):
        pass

from django.apps import AppConfig


class PsychologistConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "psychologist"
    verbose_name = "Психолог"

    def ready(self):
        import psychologist.signals  # Импортируем файл с сигналами при запуске приложения

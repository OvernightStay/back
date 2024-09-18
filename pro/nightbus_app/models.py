from django.db import models


# Абстрактный базовый класс для моделей, связанных с опытом
class ExperienceModel(models.Model):
    # Поле, указывающее, был ли получен опыт
    experience = models.BooleanField(default=False, verbose_name="Получен опыт")
    # Поле, указывающее, было ли задание не пройдено
    not_passed = models.BooleanField(default=True, verbose_name="Не пройдено")

    # Метод для обновления полей not_passed и experience на основе результата
    def update_experience(self):
        # Проверяем, есть ли у объекта поле result
        if hasattr(self, 'result'):
            # Если результат положительный, обновляем поля
            if self.result:
                self.not_passed = False  # Задание пройдено
                self.experience = True  # Опыт получен
            else:
                self.not_passed = True  # Задание не пройдено
                self.experience = False  # Опыт не получен

    # Метакласс для настройки модели
    class Meta:
        abstract = True  # Указываем, что это абстрактный класс


# Модель для новелл
class ShortStory(ExperienceModel):
    # Поле, указывающее результат прохождения новеллы
    result = models.BooleanField(default=False, verbose_name="Результат прохождения новеллы")

    # Переопределяем метод save для обновления опыта перед сохранением
    def save(self, *args, **kwargs):
        self.update_experience()  # Вызываем метод обновления опыта
        super().save(*args, **kwargs)  # Вызываем метод родительского класса

    # Метод для представления объекта в виде строки
    def __str__(self):
        return "Пройдено" if self.result else "Не пройдено"

    # Метакласс для настройки модели
    class Meta:
        verbose_name = 'Новелла'  # Одиночное название модели
        verbose_name_plural = 'Новеллы'  # Множественное название модели


# Модель для игр
class Game(ExperienceModel):
    # Поле, указывающее результат прохождения игры
    result = models.BooleanField(default=False, verbose_name="Результат прохождения игры")

    # Переопределяем метод save для обновления опыта перед сохранением
    def save(self, *args, **kwargs):
        self.update_experience()  # Вызываем метод обновления опыта
        super().save(*args, **kwargs)  # Вызываем метод родительского класса

    # Метод для представления объекта в виде строки
    def __str__(self):
        return "Пройдено" if self.result else "Не пройдено"

    # Метакласс для настройки модели
    class Meta:
        verbose_name = 'Игра'  # Одиночное название модели
        verbose_name_plural = 'Игры'  # Множественное название модели


# Модель для подарков
class Gift(models.Model):
    # Поле для названия подарка
    name = models.CharField(max_length=100, verbose_name="Название подарка")
    # Поле, указывающее, был ли подарок выдан
    awarded = models.BooleanField(default=False, verbose_name="Подарок выдан")

    # Связь с моделью ShortStory (один-ко-многим)
    short_story = models.ForeignKey(ShortStory, on_delete=models.CASCADE, verbose_name="Новелла")
    # Связь с моделью Game (один-ко-многим)
    game = models.ForeignKey(Game, on_delete=models.CASCADE, verbose_name="Игра")

    # Метод для проверки, были ли успешно пройдены новелла и игра для выдачи подарка
    def check_award(self):
        # Если новелла и игра пройдены успешно, выдаем подарок
        if self.short_story.result and self.game.result:
            self.awarded = True
            self.save(update_fields=['awarded'])  # Сохраняем только поле awarded
            return True
        return False

    # Переопределяем метод save для проверки выдачи подарка перед сохранением
    def save(self, *args, **kwargs):
        self.check_award()  # Вызываем метод проверки выдачи подарка
        super().save(*args, **kwargs)  # Вызываем метод родительского класса

    # Метакласс для настройки модели
    class Meta:
        verbose_name = "Подарок"  # Одиночное название модели
        verbose_name_plural = "Подарки"  # Множественное название модели

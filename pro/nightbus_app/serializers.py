from rest_framework import serializers
from .models import ShortStory, Game, Gift


# Создаем сериализатор для модели ShortStory
class ShortStorySerializer(serializers.ModelSerializer):
    # Внутренний класс Meta, который определяет метаданные для сериализатора
    class Meta:
        # Указываем модель, с которой будет работать сериализатор
        model = ShortStory
        # Указываем что нужно сериализовать все поля модели
        fields = '__all__'


# Создаем сериализатор для модели Game
class GameSerializer(serializers.ModelSerializer):
    # Внутренний класс Meta, который определяет метаданные для сериализатора
    class Meta:
        # Указываем модель, с которой будет работать сериализатор
        model = Game
        # Указываем что нужно сериализовать все поля модели
        fields = '__all__'


# Создаем сериализатор для модели Gift
class GiftSerializer(serializers.ModelSerializer):
    # Внутренний класс Meta, который определяет метаданные для сериализатора
    class Meta:
        # Указываем модель, с которой будет работать сериализатор
        model = Gift
        # Указываем что нужно сериализовать все поля модели
        fields = '__all__'

from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import ShortStory, Game, Gift
from .serializers import ShortStorySerializer, GameSerializer, GiftSerializer


class ShortStoryViewSet(viewsets.ModelViewSet):
    """
    Создаем ViewSet для модели ShortStory
    """
    # Указываем queryset, который будет использоваться для получения всех объектов модели ShortStory
    queryset = ShortStory.objects.all()
    # Указываем сериализатор, который будет использоваться для преобразования объектов модели в JSON и обратно
    serializer_class = ShortStorySerializer

    # Переопределяем метод create для обработки запросов на создание нового объекта ShortStory
    def create(self, request, *args, **kwargs):
        # Получаем сериализатор с данными из запроса
        serializer = self.get_serializer(data=request.data)
        # Проверяем валидность данных, и если данные не валидны, выбрасываем исключение
        serializer.is_valid(raise_exception=True)
        # Создаем новый объект ShortStory с использованием сериализатора
        self.perform_create(serializer)
        # Получаем заголовки для успешного ответа
        headers = self.get_success_headers(serializer.data)
        # Возвращаем ответ с данными нового объекта и статусом 201 (Created)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    # Переопределяем метод update для обработки запросов на обновление существующего объекта ShortStory
    def update(self, request, *args, **kwargs):
        # Определяем, является ли запрос частичным обновлением (PATCH)
        partial = kwargs.pop('partial', False)
        # Получаем объект ShortStory, который нужно обновить
        instance = self.get_object()
        # Получаем сериализатор с данными из запроса и существующим объектом
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        # Проверяем валидность данных, и если данные не валидны, выбрасываем исключение
        serializer.is_valid(raise_exception=True)
        # Обновляем объект ShortStory с использованием сериализатора
        self.perform_update(serializer)
        # Возвращаем ответ с данными обновленного объекта
        return Response(serializer.data)


class GameViewSet(viewsets.ModelViewSet):
    """
    Создаем ViewSet для модели Game
    """
    # Указываем queryset, который будет использоваться для получения всех объектов модели Game
    queryset = Game.objects.all()
    # Указываем сериализатор, который будет использоваться для преобразования объектов модели в JSON и обратно
    serializer_class = GameSerializer


class GiftViewSet(viewsets.ModelViewSet):
    """
    Создаем ViewSet для модели Gift
    """
    # Указываем queryset, который будет использоваться для получения всех объектов модели Gift
    queryset = Gift.objects.all()
    # Указываем сериализатор, который будет использоваться для преобразования объектов модели в JSON и обратно
    serializer_class = GiftSerializer

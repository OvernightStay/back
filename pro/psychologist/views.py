from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from .models import Question, Answer, QuestionProgress
from .serializers import (
    QuestionSerializer,
    AnswerSerializer,
    QuestionProgressSerializer,
    QuestionProgressCreateSerializer
)


class QuestionViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet для вопросов. Только чтение (GET).
    """
    queryset = Question.objects.prefetch_related('answers').all()
    serializer_class = QuestionSerializer


class AnswerViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet для ответов. Только чтение (GET).
    """
    queryset = Answer.objects.select_related('question').all()
    serializer_class = AnswerSerializer


class QuestionProgressViewSet(viewsets.ModelViewSet):
    """
    ViewSet для прогресса вопросов. Поддерживает создание (POST) и получение (GET).
    """
    queryset = QuestionProgress.objects.select_related('player', 'question', 'selected_answer').all()

    def get_serializer_class(self):
        # Используем разные сериализаторы для чтения и записи
        if self.action in ['create', 'update', 'partial_update']:
            return QuestionProgressCreateSerializer
        return QuestionProgressSerializer

    def create(self, request, *args, **kwargs):
        """
        Метод создания прогресса вопроса. Переопределен для валидации данных.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'])
    def player_progress(self, request, *args, **kwargs):
        """
        Дополнительное действие для получения прогресса вопросов для конкретного игрока.
        Использует GET параметр player_id.
        """
        player_id = request.query_params.get('player_id')
        if not player_id:
            return Response({"detail": "player_id is required."}, status=status.HTTP_400_BAD_REQUEST)

        progress = QuestionProgress.objects.filter(player_id=player_id).select_related('question', 'selected_answer')
        serializer = self.get_serializer(progress, many=True)
        return Response(serializer.data)

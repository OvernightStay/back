from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import MiniNovella, MiniGame, PlayerProgress, Reward
from .serializers import MiniNovellaSerializer, MiniGameSerializer, PlayerProgressSerializer, RewardSerializer
from user_app.models import Player


# Представление для мини-новелл
class MiniNovellaViewSet(viewsets.ModelViewSet):
    queryset = MiniNovella.objects.all()
    serializer_class = MiniNovellaSerializer


# Представление для мини-игр
class MiniGameViewSet(viewsets.ModelViewSet):
    queryset = MiniGame.objects.all()
    serializer_class = MiniGameSerializer


# Представление для прогресса игрока
class PlayerProgressViewSet(viewsets.ModelViewSet):
    queryset = PlayerProgress.objects.all()
    serializer_class = PlayerProgressSerializer

    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        """Метод для завершения новеллы или игры и начисления опыта"""
        progress = self.get_object()

        # Логика завершения и начисления опыта
        if not progress.completed:
            progress.complete_progress()
            serializer = self.get_serializer(progress)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"detail": "Already completed"}, status=status.HTTP_400_BAD_REQUEST)

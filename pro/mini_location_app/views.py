from rest_framework import viewsets
from .models import (
    PlayerProgress,
    MiniNovella,
    MiniGame,
    EmployeeGame,
    Reward,
    PlayerNovellaProgress,
    PlayerGameProgress,
    PlayerEmployeeGameProgress,
    PlayerRewardProgress,
)
from .serializers import (
    PlayerProgressSerializer,
    MiniNovellaSerializer,
    MiniGameSerializer,
    EmployeeGameSerializer,
    RewardSerializer,
    PlayerNovellaProgressSerializer,
    PlayerGameProgressSerializer,
    PlayerEmployeeGameProgressSerializer,
    PlayerRewardProgressSerializer,
)


class MiniNovellaViewSet(viewsets.ModelViewSet):
    queryset = MiniNovella.objects.all()
    serializer_class = MiniNovellaSerializer


class MiniGameViewSet(viewsets.ModelViewSet):
    queryset = MiniGame.objects.all()
    serializer_class = MiniGameSerializer


class EmployeeGameViewSet(viewsets.ModelViewSet):
    queryset = EmployeeGame.objects.all()
    serializer_class = EmployeeGameSerializer


class RewardViewSet(viewsets.ModelViewSet):
    queryset = Reward.objects.all()
    serializer_class = RewardSerializer


class PlayerProgressViewSet(viewsets.ModelViewSet):
    queryset = PlayerProgress.objects.prefetch_related(
        "novella_progress__novella",
        "game_progress__game",
        "employee_game_progress__employee_game",
        "reward_progress__reward",
    ).select_related("player")
    serializer_class = PlayerProgressSerializer


class PlayerNovellaProgressViewSet(viewsets.ModelViewSet):
    queryset = PlayerNovellaProgress.objects.select_related(
        "player_progress", "novella"
    )
    serializer_class = PlayerNovellaProgressSerializer


class PlayerGameProgressViewSet(viewsets.ModelViewSet):
    queryset = PlayerGameProgress.objects.select_related("player_progress", "game")
    serializer_class = PlayerGameProgressSerializer


class PlayerEmployeeGameProgressViewSet(viewsets.ModelViewSet):
    queryset = PlayerEmployeeGameProgress.objects.select_related(
        "player_progress", "employee_game"
    )
    serializer_class = PlayerEmployeeGameProgressSerializer


class PlayerRewardProgressViewSet(viewsets.ModelViewSet):
    queryset = PlayerRewardProgress.objects.select_related("player_progress", "reward")
    serializer_class = PlayerRewardProgressSerializer

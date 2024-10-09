from rest_framework.routers import DefaultRouter
from .views import (
    MiniNovellaViewSet, MiniGameViewSet, EmployeeGameViewSet, RewardViewSet,
    PlayerProgressViewSet, PlayerNovellaProgressViewSet, PlayerGameProgressViewSet,
    PlayerEmployeeGameProgressViewSet, PlayerRewardProgressViewSet
)

router = DefaultRouter()
router.register(r'mini-novellas', MiniNovellaViewSet)
router.register(r'mini-games', MiniGameViewSet)
router.register(r'employee-games', EmployeeGameViewSet)
router.register(r'rewards', RewardViewSet)
router.register(r'player-progress', PlayerProgressViewSet)
router.register(r'player-novella-progress', PlayerNovellaProgressViewSet)
router.register(r'player-game-progress', PlayerGameProgressViewSet)
router.register(r'player-employee-game-progress', PlayerEmployeeGameProgressViewSet)
router.register(r'player-reward-progress', PlayerRewardProgressViewSet)

urlpatterns = router.urls

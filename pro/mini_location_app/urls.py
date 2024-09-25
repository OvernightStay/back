from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'novellas', MiniNovellaViewSet, basename='mini-novella')
router.register(r'games', MiniGameViewSet, basename='mini-game')
router.register(r'progress', PlayerProgressViewSet, basename='player-progress')
router.register(r'rewards', RewardViewSet)
router.register(r'Employee', EmployeeGameViewSet)

urlpatterns = router.urls

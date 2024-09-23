from rest_framework.routers import DefaultRouter
from .views import MiniNovellaViewSet, MiniGameViewSet, PlayerProgressViewSet

router = DefaultRouter()
router.register(r'novellas', MiniNovellaViewSet, basename='mini-novella')
router.register(r'games', MiniGameViewSet, basename='mini-game')
router.register(r'progress', PlayerProgressViewSet, basename='player-progress')

urlpatterns = router.urls

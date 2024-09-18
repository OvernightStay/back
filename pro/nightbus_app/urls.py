from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views
from .views import ShortStoryViewSet, GameViewSet, GiftViewSet

# Создаем экземпляр DefaultRouter, который будет управлять маршрутами.
router = DefaultRouter()

# Регистрируем ShortStoryViewSet с префиксом 'shortstories'.
router.register(r'shortstories', ShortStoryViewSet)
# Регистрируем GameViewSet с префиксом 'games'.
router.register(r'games', GameViewSet)
# Регистрируем GiftViewSet с префиксом 'gifts'.
router.register(r'gifts', GiftViewSet)
# Определяем список URL-шаблонов для нашего приложения.

urlpatterns = [
    # Включаем все URL-маршруты, сгенерированные DefaultRouter, в корневой путь '/'.
    path('', include(router.urls)),
]

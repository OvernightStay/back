from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import QuestionViewSet, AnswerViewSet, PsychoProgressViewSet

# Создаем маршрутизатор и регистрируем наши ViewSet
router = DefaultRouter()
router.register(r'questions', QuestionViewSet, basename='question')
router.register(r'answers', AnswerViewSet, basename='answer')
router.register(r'progress', PsychoProgressViewSet, basename='psychoprogress')


# Определяем urlpatterns
urlpatterns = [
    path('', include(router.urls)),  # Включаем маршруты из роутера
]

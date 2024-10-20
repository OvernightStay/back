from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import QuestionViewSet, AnswerViewSet, QuestionProgressViewSet, SendTestResultsView

# Создаем роутер и регистрируем ViewSet'ы
router = DefaultRouter()
router.register(r'questions', QuestionViewSet, basename='questions')
router.register(r'answers', AnswerViewSet, basename='answers')
router.register(r'progress', QuestionProgressViewSet, basename='progress')

urlpatterns = [
    path('', include(router.urls)),  # Подключаем все маршруты, созданные роутером
    path('send-results/<int:player_id>/', SendTestResultsView.as_view(), name='send_test_results'),

]

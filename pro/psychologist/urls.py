from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import QuestionViewSet, TestProgressViewSet

router = DefaultRouter()
router.register(r'questions', QuestionViewSet)
router.register(r'test-progress', TestProgressViewSet)  # Новый маршрут для отслеживания прогресса

urlpatterns = [
    path('', include(router.urls)),
]

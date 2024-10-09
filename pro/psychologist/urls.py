from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import QuestionViewSet, AnswerViewSet, QuestionTransitionViewSet, PsychoProgressViewSet

router = DefaultRouter()
router.register(r'questions', QuestionViewSet)
router.register(r'answers', AnswerViewSet)
router.register(r'question-transitions', QuestionTransitionViewSet)
router.register(r'psycho-progress', PsychoProgressViewSet)

urlpatterns = [
    path('', include(router.urls)),  # Включение маршрутов
]

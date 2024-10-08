from django.urls import path

from .views import QuestionDetailView, QuestionViewSet, AnswerViewSet

urlpatterns = [
    path('questions/<int:question_id>/', QuestionDetailView.as_view(), name='question-detail'),
    path('questions/', QuestionViewSet.as_view({'get': 'list'})),
    path('answers/', AnswerViewSet.as_view({'get': 'list'})),
]

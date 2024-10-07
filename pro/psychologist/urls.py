from django.urls import path
from .views import QuestionDetailView

urlpatterns = [
    path('questions/<int:question_id>/', QuestionDetailView.as_view(), name='question-detail'),
]

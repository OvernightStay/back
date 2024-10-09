from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Question, Answer, QuestionTransition, PsychoProgress
from .serializers import QuestionSerializer, AnswerSerializer, QuestionTransitionSerializer, PsychoProgressSerializer


# Представление для модели Question
class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.select_related('answers').all()
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated]


# Представление для модели Answer
class AnswerViewSet(viewsets.ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = [IsAuthenticated]


# Представление для модели QuestionTransition
class QuestionTransitionViewSet(viewsets.ModelViewSet):
    queryset = QuestionTransition.objects.all()
    serializer_class = QuestionTransitionSerializer
    permission_classes = [IsAuthenticated]


# Представление для модели PsychoProgress
class PsychoProgressViewSet(viewsets.ModelViewSet):
    queryset = PsychoProgress.objects.select_related('player', 'current_question').prefetch_related(
        'selected_answers').all()
    serializer_class = PsychoProgressSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(player=self.request.user)  # Привязываем прогресс к текущему пользователю

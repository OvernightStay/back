from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Question, Answer, QuestionTransition, PsychoProgress
from .serializers import (
    QuestionSerializer,
    AnswerSerializer,
    QuestionTransitionSerializer,
    PsychoProgressSerializer,
)


# Представление для модели Question
class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.select_related("answers").all()
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
    queryset = (
        PsychoProgress.objects.select_related("player", "current_question")
        .prefetch_related("selected_answers")
        .all()
    )
    serializer_class = PsychoProgressSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(player=self.request.user)

    def update(self, request, *args, **kwargs):
        progress = self.get_object()
        answer_id = request.data.get("answer_id")
        if not answer_id:
            return Response(
                {"error": "Answer ID required"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            answer = Answer.objects.get(id=answer_id)
        except Answer.DoesNotExist:
            return Response(
                {"error": "Answer not found"}, status=status.HTTP_404_NOT_FOUND
            )

        # Сохраняем выбранный ответ и ищем следующий вопрос
        progress.selected_answers.add(answer)
        progress.next_question(answer)

        # Возвращаем следующее состояние
        if progress.completed:
            progress.send_results_email()
            return Response({"message": "Test completed"}, status=status.HTTP_200_OK)
        else:
            return Response(PsychoProgressSerializer(progress).data)

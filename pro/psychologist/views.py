from rest_framework import viewsets, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Question, PsychoProgress, Answer
from .serializers import QuestionSerializer, AnswerSerializer, PsychoProgressSerializer


class QuestionViewSet(viewsets.ViewSet):
    def retrieve(self, request, pk=None):
        player = request.user  # Текущий игрок

        # Получаем прогресс игрока или создаём новый
        progress, created = PsychoProgress.objects.get_or_create(player=player, completed=False)

        # Если указан pk (question_id), проверяем его, иначе возвращаем текущий вопрос игрока
        if pk:
            question = get_object_or_404(Question, id=pk)
        else:
            question = progress.current_question

        if not question:
            return Response({"message": "Test completed or no current question"}, status=status.HTTP_200_OK)

        serializer = QuestionSerializer(question)
        return Response(serializer.data)

    def create(self, request, pk=None):
        player = request.user  # Текущий игрок
        progress = get_object_or_404(PsychoProgress, player=player, completed=False)

        try:
            question = Question.objects.get(id=pk)
        except Question.DoesNotExist:
            return Response({"error": "Question not found"}, status=status.HTTP_404_NOT_FOUND)

        selected_answer_id = request.data.get('answer_id')
        selected_answer = get_object_or_404(Answer, id=selected_answer_id, question=question)

        # Сохраняем ответ игрока
        progress.selected_answers.add(selected_answer)

        # Определяем следующий вопрос
        if selected_answer.is_first_option:
            next_question = question.next_question_if_first_answer
        else:
            next_question = question.next_question_if_second_answer

        # Обновляем текущий вопрос игрока
        progress.current_question = next_question
        if not next_question:
            progress.completed = True  # Тест завершён
        progress.save()

        if next_question:
            serializer = QuestionSerializer(next_question)
            return Response(serializer.data)
        else:
            return Response({"message": "Test completed"}, status=status.HTTP_200_OK)


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class AnswerViewSet(viewsets.ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer


class PsychoProgressViewSet(viewsets.ModelViewSet):
    queryset = PsychoProgress.objects.all()
    serializer_class = PsychoProgressSerializer

    def get_queryset(self):
        # Ограничим выборку только прогрессом текущего игрока
        return self.queryset.filter(player=self.request.user)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        # Позволим создавать только прогресс для текущего игрока
        request.data['player'] = request.user.id
        return super().create(request, *args, **kwargs)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from .models import Question, Answer, PsychoProgress
from .serializers import QuestionSerializer, AnswerSerializer
from django.shortcuts import get_object_or_404


class QuestionDetailView(APIView):
    def get(self, request, question_id=None):
        player = request.user  # Текущий игрок

        # Получаем прогресс игрока или создаём новый
        progress, created = PsychoProgress.objects.get_or_create(player=player, completed=False)

        # Если указан question_id, проверяем его, иначе возвращаем текущий вопрос игрока
        if question_id:
            question = get_object_or_404(Question, id=question_id)
        else:
            question = progress.current_question

        if not question:
            return Response({"message": "Test completed or no current question"}, status=status.HTTP_200_OK)

        serializer = QuestionSerializer(question)
        return Response(serializer.data)

    def post(self, request, question_id):
        player = request.user  # Текущий игрок
        progress = get_object_or_404(PsychoProgress, player=player, completed=False)

        try:
            question = Question.objects.get(id=question_id)
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

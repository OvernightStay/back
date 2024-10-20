from rest_framework import viewsets
from .models import Question, Answer, QuestionProgress
from .serializers import QuestionSerializer, AnswerSerializer, QuestionProgressSerializer


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class AnswerViewSet(viewsets.ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer


class QuestionProgressViewSet(viewsets.ModelViewSet):
    queryset = QuestionProgress.objects.all()
    serializer_class = QuestionProgressSerializer

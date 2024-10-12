from rest_framework import viewsets
from .models import Question, TestProgress
from .serializers import QuestionSerializer, TestProgressSerializer


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class TestProgressViewSet(viewsets.ModelViewSet):
    queryset = TestProgress.objects.all()
    serializer_class = TestProgressSerializer

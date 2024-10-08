from rest_framework import serializers
from .models import Question, Answer, PsychoProgress


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'text', 'is_first_option']


class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'text', 'answers']


class PsychoProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = PsychoProgress
        fields = '__all__'  # Или укажите конкретные поля

from rest_framework import serializers
from .models import Question, Answer, TestProgress


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'text', 'number']


class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True)  # Включаем список ответов
    question_number = serializers.ReadOnlyField()  # Поле для уникального номера вопроса

    class Meta:
        model = Question
        fields = ['id', 'text', 'question_number', 'answers']
        read_only_fields = ['question_number']  # Номер вопроса присваивается автоматически

    def create(self, validated_data):
        answers_data = validated_data.pop('answers')
        question = Question.objects.create(**validated_data)
        for answer_data in answers_data:
            Answer.objects.create(question=question, **answer_data)
        return question


class TestProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestProgress
        fields = ['id', 'player', 'question', 'selected_answer', 'completed_at']
        read_only_fields = ['completed_at']

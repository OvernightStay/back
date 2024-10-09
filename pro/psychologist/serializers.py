from rest_framework import serializers
from .models import Question, Answer, QuestionTransition, PsychoProgress


# Сериализатор для модели Answer
class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'question', 'text', 'order']  # Поля, которые нужно включить в сериализацию


# Сериализатор для модели Question
class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, read_only=True)  # Вложенные ответы

    class Meta:
        model = Question
        fields = ['id', 'text', 'answers']  # Поля, которые нужно включить в сериализацию


# Сериализатор для модели QuestionTransition
class QuestionTransitionSerializer(serializers.ModelSerializer):
    question = QuestionSerializer(read_only=True)
    answer = AnswerSerializer(read_only=True)
    next_question = QuestionSerializer(read_only=True)

    class Meta:
        model = QuestionTransition
        fields = ['id', 'question', 'answer', 'next_question']  # Поля, которые нужно включить в сериализацию


# Сериализатор для модели PsychoProgress
class PsychoProgressSerializer(serializers.ModelSerializer):
    player = serializers.StringRelatedField()  # Отображение игрока по строковому представлению
    current_question = QuestionSerializer(read_only=True)
    selected_answers = AnswerSerializer(many=True, read_only=True)

    class Meta:
        model = PsychoProgress
        fields = ['id', 'player', 'current_question', 'selected_answers',
                  'completed']  # Поля, которые нужно включить в сериализацию

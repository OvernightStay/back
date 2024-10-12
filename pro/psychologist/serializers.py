from rest_framework import serializers
from .models import Question, Answer, QuestionProgress


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'text', 'number']  # Поля, которые будут отображены в API


class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, read_only=True)  # Вложенные ответы

    class Meta:
        model = Question
        fields = ['id', 'text', 'question_number', 'answers']  # Поля для отображения в API


class QuestionProgressSerializer(serializers.ModelSerializer):
    player = serializers.StringRelatedField()  # Отображение игрока как строки
    question = QuestionSerializer()  # Вложенный сериализатор вопроса
    selected_answer = AnswerSerializer()  # Вложенный сериализатор выбранного ответа

    class Meta:
        model = QuestionProgress
        fields = ['id', 'player', 'question', 'selected_answer']  # Поля для отображения в API


class QuestionProgressCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания прогресса вопроса"""

    class Meta:
        model = QuestionProgress
        fields = ['id', 'player', 'question', 'selected_answer']

    def validate(self, data):
        # Проверка на то, что выбранный ответ относится к заданному вопросу
        selected_answer = data.get('selected_answer')
        question = data.get('question')

        if selected_answer and selected_answer.question != question:
            raise serializers.ValidationError("Выбранный ответ не относится к данному вопросу.")

        return data

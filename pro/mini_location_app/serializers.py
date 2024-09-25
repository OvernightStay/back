from rest_framework import serializers
from .models import *


class MiniNovellaSerializer(serializers.ModelSerializer):
    class Meta:
        model = MiniNovella
        fields = '__all__'


class MiniGameSerializer(serializers.ModelSerializer):
    class Meta:
        model = MiniGame
        fields = '__all__'


class EmployeeGameSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeGame
        fields = '__all__'


class RewardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reward
        fields = '__all__'


class PlayerProgressSerializer(serializers.ModelSerializer):
    novella = MiniNovellaSerializer(many=True, read_only=True)
    game = MiniGameSerializer(many=True, read_only=True)
    reward = RewardSerializer(many=True, read_only=True)

    class Meta:
        model = PlayerProgress
        fields = '__all__'

from rest_framework import serializers
from .models import (
    PlayerProgress, MiniNovella, MiniGame, EmployeeGame,
    Reward, PlayerNovellaProgress, PlayerGameProgress,
    PlayerEmployeeGameProgress, PlayerRewardProgress
)


class MiniNovellaSerializer(serializers.ModelSerializer):
    class Meta:
        model = MiniNovella
        fields = ['id', 'title']


class MiniGameSerializer(serializers.ModelSerializer):
    class Meta:
        model = MiniGame
        fields = ['id', 'title']


class EmployeeGameSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeGame
        fields = ['id', 'title']


class RewardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reward
        fields = ['id', 'title']


class PlayerProgressSerializer(serializers.ModelSerializer):
    player = serializers.StringRelatedField()  # В случае, если в Player есть login
    novella_progress = serializers.SerializerMethodField()
    game_progress = serializers.SerializerMethodField()
    employee_game_progress = serializers.SerializerMethodField()
    reward_progress = serializers.SerializerMethodField()

    class Meta:
        model = PlayerProgress
        fields = [
            'id', 'player', 'experience_gained',
            'completion_time', 'novella_progress', 'game_progress',
            'employee_game_progress', 'reward_progress'
        ]

    def get_novella_progress(self, obj):
        return PlayerNovellaProgressSerializer(obj.novella_progress.all(), many=True).data

    def get_game_progress(self, obj):
        return PlayerGameProgressSerializer(obj.game_progress.all(), many=True).data

    def get_employee_game_progress(self, obj):
        return PlayerEmployeeGameProgressSerializer(obj.employee_game_progress.all(), many=True).data

    def get_reward_progress(self, obj):
        return PlayerRewardProgressSerializer(obj.reward_progress.all(), many=True).data


class PlayerNovellaProgressSerializer(serializers.ModelSerializer):
    novella = MiniNovellaSerializer()

    class Meta:
        model = PlayerNovellaProgress
        fields = ['id', 'novella']


class PlayerGameProgressSerializer(serializers.ModelSerializer):
    game = MiniGameSerializer()

    class Meta:
        model = PlayerGameProgress
        fields = ['id', 'game']


class PlayerEmployeeGameProgressSerializer(serializers.ModelSerializer):
    employee_game = EmployeeGameSerializer()

    class Meta:
        model = PlayerEmployeeGameProgress
        fields = ['id', 'employee_game']


class PlayerRewardProgressSerializer(serializers.ModelSerializer):
    reward = RewardSerializer()

    class Meta:
        model = PlayerRewardProgress
        fields = ['id', 'reward']

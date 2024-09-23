from rest_framework import serializers
from .models import MiniNovella, MiniGame, PlayerProgress, Reward


class MiniNovellaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MiniNovella
        fields = ['id', 'title', 'description']


class MiniGameSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MiniGame
        fields = ['id', 'title', 'description']


class RewardSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Reward
        fields = ['id', 'title', 'unique_code']


class PlayerProgressSerializer(serializers.HyperlinkedModelSerializer):
    novella = MiniNovellaSerializer(read_only=True)
    game = MiniGameSerializer(read_only=True)
    reward = serializers.CharField(read_only=True)

    class Meta:
        model = PlayerProgress
        fields = ['id', 'player', 'novella', 'game', 'completed', 'experience_gained', 'reward', 'completion_time']
        read_only_fields = ['experience_gained', 'reward', 'completed', 'completion_time']

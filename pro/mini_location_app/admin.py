from django.contrib import admin
from .models import (
    PlayerProgress,
    MiniNovella,
    MiniGame,
    EmployeeGame,
    Reward,
    PlayerNovellaProgress,
    PlayerGameProgress,
    PlayerEmployeeGameProgress,
    PlayerRewardProgress,
)


# Inline для промежуточных моделей
class PlayerNovellaProgressInline(admin.TabularInline):
    model = PlayerNovellaProgress
    extra = 1
    autocomplete_fields = ["novella"]  # Чтобы было удобнее выбирать связанные объекты


class PlayerGameProgressInline(admin.TabularInline):
    model = PlayerGameProgress
    extra = 1
    autocomplete_fields = ["game"]


class PlayerEmployeeGameProgressInline(admin.TabularInline):
    model = PlayerEmployeeGameProgress
    extra = 1
    autocomplete_fields = ["employee_game"]


class PlayerRewardProgressInline(admin.TabularInline):
    model = PlayerRewardProgress
    extra = 1
    autocomplete_fields = ["reward"]


# Админка для PlayerProgress с инлайнами
@admin.register(PlayerProgress)
class PlayerProgressAdmin(admin.ModelAdmin):
    list_display = ["player", "experience_gained", "completion_time"]
    list_filter = ["completion_time", "player"]
    search_fields = ["player__login"]
    inlines = [
        PlayerNovellaProgressInline,
        PlayerGameProgressInline,
        PlayerEmployeeGameProgressInline,
        PlayerRewardProgressInline,
    ]
    autocomplete_fields = ["player"]


# Админка для MiniNovella
@admin.register(MiniNovella)
class MiniNovellaAdmin(admin.ModelAdmin):
    list_display = ["title"]
    search_fields = ["title"]


# Админка для MiniGame
@admin.register(MiniGame)
class MiniGameAdmin(admin.ModelAdmin):
    list_display = ["title"]
    search_fields = ["title"]


# Админка для EmployeeGame
@admin.register(EmployeeGame)
class EmployeeGameAdmin(admin.ModelAdmin):
    list_display = ["title"]
    search_fields = ["title"]


# Админка для Reward
@admin.register(Reward)
class RewardAdmin(admin.ModelAdmin):
    list_display = ["title"]
    search_fields = ["title"]

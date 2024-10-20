from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.utils import timezone
from .models import Backpack, BackpackItem, Item

Player = get_user_model()


class PlayerRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ["login", "email", "phone", "password", "first_name", "last_name"]
        extra_kwargs = {
            "password": {"write_only": True},
            "email": {"required": False, "allow_blank": True},
        }

    def validate_phone(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("Phone number must contain only digits.")
        if len(value) != 11:
            raise serializers.ValidationError("Phone number must be exactly 11 digits.")
        return value

    def create(self, validated_data):
        player = Player.objects.create_user(
            login=validated_data["login"],
            email=validated_data.get("email", None),
            phone=validated_data["phone"],
            password=validated_data["password"],
            first_name=validated_data.get("first_name", ""),
            last_name=validated_data.get("last_name", ""),
        )
        return player


class PlayerLoginSerializer(serializers.Serializer):
    login = serializers.CharField(required=True)
    password = serializers.CharField(required=True)


# class VerifyCodeSerializer(serializers.Serializer):
#     code = serializers.CharField(required=True)


class PlayerSerializer(serializers.ModelSerializer):
    current_password = serializers.CharField(write_only=True, required=False)
    new_password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Player
        fields = [
            "id",
            "username",
            "login",
            "email",
            "phone",
            "first_name",
            "last_name",
            "gender",
            "training_check",
            "current_password",
            "new_password",
        ]

    def validate_login(self, value):
        if Player.objects.filter(login=value).exclude(id=self.instance.id).exists():
            raise serializers.ValidationError("This login is already in use.")
        return value

    def validate_email(self, value):
        if Player.objects.filter(email=value).exclude(id=self.instance.id).exists():
            raise serializers.ValidationError("This email is already in use.")
        return value

    def validate_phone(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("Phone number must contain only digits.")
        if len(value) != 11:
            raise serializers.ValidationError("Phone number must be exactly 11 digits.")
        if Player.objects.filter(phone=value).exclude(id=self.instance.id).exists():
            raise serializers.ValidationError("This phone number is already in use.")
        return value

    def validate_new_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError(
                "Password must be at least 8 characters long."
            )
        return value


# Восстановление доступа
class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not Player.objects.filter(email=value).exists():
            raise serializers.ValidationError("User with this email does not exist.")
        return value


class PasswordResetConfirmSerializer(serializers.Serializer):
    code = serializers.CharField()

    def validate_code(self, value):
        if not value.isdigit() or len(value) != 6:
            raise serializers.ValidationError("Invalid code.")
        return value

    def validate(self, attrs):
        code = attrs.get("code")
        try:
            player = Player.objects.get(verification_code=code)
        except Player.DoesNotExist:
            raise serializers.ValidationError("Invalid code or email.")

        if player.code_expiry < timezone.now():
            raise serializers.ValidationError("The code has expired.")

        return attrs


######### Для рюкзака: #########
# Предметы
class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = "__all__"


# Позиции предметов в рюкзаке
class BackpackItemSerializer(serializers.ModelSerializer):
    item = serializers.PrimaryKeyRelatedField(queryset=Item.objects.all())
    item_title = serializers.SerializerMethodField()
    item_description = serializers.SerializerMethodField()
    item_image = serializers.SerializerMethodField()

    class Meta:
        model = BackpackItem
        fields = ["id", "item", "item_title", "item_description", "item_image"]
        read_only_fields = ["backpack"]


# Рюкзак
class BackpackSerializer(serializers.ModelSerializer):
    items = BackpackItemSerializer(many=True, source="backpackitem_set", read_only=True)
    player = PlayerSerializer(read_only=True)

    class Meta:
        model = Backpack
        fields = ["id", "player", "items", "created_at"]

    # Добавление игрока в поле для создания его рюкзака
    def create(self, validated_data):
        player = self.context.get("player")
        if player:
            validated_data["player"] = player
        return super().create(validated_data)

    def validate(self, data):
        player = self.context.get("player")
        if Backpack.objects.filter(player=player).exists():
            raise serializers.ValidationError("У вас уже есть рюкзак.")
        return data

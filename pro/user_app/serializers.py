from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.utils import timezone

Player = get_user_model()

class PlayerRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ['phone', 'email', 'password', 'first_name', 'last_name']
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    def validate_phone(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("Phone number must contain only digits.")
        if len(value) != 11:
            raise serializers.ValidationError("Phone number must be exactly 11 digits.")
        return value
    
    def create(self, validated_data):
        player = Player.objects.create_user(
            phone=validated_data['phone'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        return player


class PlayerLoginSerializer(serializers.Serializer):
    login = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    
    def validate_login(self, value):
        if '@' in value:
            return value
        elif value.isdigit() and len(value) == 11:
            return value
        else:
            raise serializers.ValidationError("Login must be a valid email or phone number.")


class VerifyCodeSerializer(serializers.Serializer):
    code = serializers.CharField(required=True)


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ['id', 'email', 'phone', 'first_name', 'last_name']
        
    def validate_phone(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("Phone number must contain only digits.")
        if len(value) != 11:
            raise serializers.ValidationError("Phone number must be exactly 11 digits.")
        if Player.objects.filter(phone=value).exclude(id=self.instance.id).exists():
            raise serializers.ValidationError("This phone number is already in use.")
        return value

    def validate_email(self, value):
        if Player.objects.filter(email=value).exclude(id=self.instance.id).exists():
            raise serializers.ValidationError("This email is already in use.")
        return value


# Восстановление доступа (смена пароля)
class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not Player.objects.filter(email=value).exists():
            raise serializers.ValidationError("User with this email does not exist.")
        return value


class PasswordResetConfirmSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField()
    new_password = serializers.CharField()

    def validate_code(self, value):
        if not value.isdigit() or len(value) != 6:
            raise serializers.ValidationError("Invalid code.")
        return value

    def validate_new_password(self, value):
        # Добавьте здесь дополнительные проверки пароля, если нужно
        return value

    def validate(self, attrs):
        email = attrs.get('email')
        code = attrs.get('code')
        try:
            player = Player.objects.get(email=email, verification_code=code)
        except Player.DoesNotExist:
            raise serializers.ValidationError("Invalid code or email.")
        
        if player.code_expiry < timezone.now():
            raise serializers.ValidationError("The code has expired.")
        
        return attrs

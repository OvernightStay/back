from django.contrib.auth import authenticate, login as auth_login, logout
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import SessionAuthentication
from django.contrib.auth import get_user_model
from .serializers import *
from .utils import send_verification_code_email
from .authentication import get_backend_name

Player = get_user_model()

def get_tokens_for_player(player):
    refresh = RefreshToken.for_user(player)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class PlayerRegisterViewSet(APIView):
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = PlayerRegisterSerializer(data=request.data)
        if serializer.is_valid():
            player = serializer.save()
            code = player.generate_verification_code()
            send_verification_code_email(player.email, code)
            return Response({'detail': 'Verification code sent for new user'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PlayerLoginViewSet(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = PlayerLoginSerializer(data=request.data)
        if serializer.is_valid():
            login = serializer.validated_data.get('login')
            password = serializer.validated_data.get('password')
            
            player = authenticate(request, username=login, password=password)
            
            if player is not None:
                if not player.is_active:
                    code = player.generate_verification_code()
                    send_verification_code_email(player.email, code)
                    return Response({'detail': 'Account is not activated. Verification code sent again.'}, status=status.HTTP_400_BAD_REQUEST)
                
                auth_login(request, player, backend=get_backend_name())
                tokens = get_tokens_for_player(player)
                return Response({'detail': 'Login successful', 'tokens': tokens}, status=status.HTTP_200_OK)
            else:
                return Response({'detail': 'Invalid login credentials'}, status=status.HTTP_400_BAD_REQUEST)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyCodeViewSet(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = VerifyCodeSerializer(data=request.data)
        if serializer.is_valid():
            code = serializer.validated_data.get('code')
            player = Player.objects.filter(verification_code=code).first()
            
            if player and player.code_expiry > timezone.now():
                player.verification_code = None
                player.code_expiry = None
                player.is_active = True  # Активация аккаунта после успешной верификации
                player.save()
                auth_login(request, player, backend=get_backend_name())
                tokens = get_tokens_for_player(player)
                return Response({'detail': 'Login successful', 'tokens': tokens}, status=status.HTTP_200_OK)
            
            return Response({'detail': 'Invalid or expired code'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PlayerLogoutViewSet(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response(status=status.HTTP_200_OK)


class PlayerViewSet(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication, SessionAuthentication]

    def get(self, request):
        serializer = PlayerSerializer(request.user)
        return Response({'player': serializer.data}, status=status.HTTP_200_OK)

    def put(self, request):
        serializer = PlayerSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'player': serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Восстановление доступа (смена пароля)
class PasswordResetRequestView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            player = Player.objects.get(email=email)
            code = player.generate_verification_code()
            send_verification_code_email(email, code)
            return Response({'detail': 'Verification code sent.'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetConfirmView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            new_password = serializer.validated_data['new_password']
            player = Player.objects.get(email=email)
            player.set_password(new_password)
            player.verification_code = None
            player.code_expiry = None
            player.save()
            auth_login(request, player, backend=get_backend_name())
            return Response({'detail': 'Password has been reset.'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from django.contrib.auth import authenticate, login as auth_login, logout
from django.utils import timezone
from rest_framework import permissions, status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import SessionAuthentication
from django.contrib.auth import get_user_model
from .serializers import *
from .utils import send_verification_code_email

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
            serializer.save()
            return Response({'detail': 'Register successful'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PlayerLoginViewSet(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = PlayerLoginSerializer(data=request.data)
        if serializer.is_valid():
            login = serializer.validated_data.get('login')
            password = serializer.validated_data.get('password')
            player = authenticate(request, username=login, password=password)
            auth_login(request, player, backend='django.contrib.auth.backends.ModelBackend')
            tokens = get_tokens_for_player(player)
            return Response({'detail': 'Login successful', 'tokens': tokens}, status=status.HTTP_200_OK)
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
        player = request.user
        serializer = PlayerSerializer(player, data=request.data, partial=True)
        if serializer.is_valid():
            if 'current_password' in request.data and 'new_password' in request.data:
                current_password = request.data.get('current_password')
                if not player.check_password(current_password):
                    return Response({'detail': 'Current password is incorrect.'}, status=status.HTTP_400_BAD_REQUEST)
                
                new_password = request.data.get('new_password')
                player.set_password(new_password)
                player.save()
                return Response({'detail': 'Password has been updated successfully.'}, status=status.HTTP_200_OK)
            
            elif 'new_password' in request.data:
                new_password = request.data.get('new_password')
                player.set_password(new_password)
                player.save()
                return Response({'detail': 'Password has been updated successfully.'}, status=status.HTTP_200_OK)
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
            code = serializer.validated_data['code']
            player = Player.objects.get(verification_code=code)
            player.verification_code = None
            player.code_expiry = None
            player.save()
            auth_login(request, player, backend='django.contrib.auth.backends.ModelBackend')
            return Response({'detail': 'Password has been reset.'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


######### Для рюкзака: #########
# Предметы
class ItemViewSet(generics.ListCreateAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            self.permission_classes = [permissions.AllowAny]
        else:
            self.permission_classes = [permissions.IsAdminUser]
        return super().get_permissions()


# Рюкзак
class BackpackViewSet(generics.ListAPIView):
    queryset = Backpack.objects.all()
    serializer_class = BackpackSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Backpack.objects.filter(player=self.request.user)


# Позиции предметов в рюкзаке
class BackpackItemViewSet(generics.ListCreateAPIView):
    serializer_class = BackpackItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    # Сохраняет рюкзак игрока
    def get_serializer_context(self):
        context = super().get_serializer_context()
        backpack = Backpack.objects.get(player=self.request.user)
        context.update({
            'backpack': backpack,
        })
        return context

    # Выдаются только позиции игрока
    def get_queryset(self):
        return BackpackItem.objects.filter(backpack__player=self.request.user)

    def perform_create(self, serializer):
        backpack = Backpack.objects.get(player=self.request.user)
        item = serializer.validated_data['item']

        # Проверка, существует ли уже предмет в рюкзаке
        existing_item = BackpackItem.objects.filter(backpack=backpack, item=item).first()

        if not existing_item:
            # Создание нового элемента рюкзака
            serializer.save(backpack=backpack)


# class VerifyCodeViewSet(APIView):
#     permission_classes = [permissions.AllowAny]

#     def post(self, request):
#         serializer = VerifyCodeSerializer(data=request.data)
#         if serializer.is_valid():
#             code = serializer.validated_data.get('code')
#             player = Player.objects.filter(verification_code=code).first()
            
#             if player and player.code_expiry > timezone.now():
#                 player.verification_code = None
#                 player.code_expiry = None
#                 player.is_active = True  # Активация аккаунта после успешной верификации
#                 player.save()
#                 # auth_login(request, player, backend=get_backend_name())
#                 # tokens = get_tokens_for_player(player)
#                 return Response({'detail': 'Register successful'}, status=status.HTTP_200_OK)
            
#             return Response({'detail': 'Invalid or expired code'}, status=status.HTTP_400_BAD_REQUEST)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

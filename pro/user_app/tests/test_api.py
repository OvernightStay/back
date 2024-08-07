from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from user_app.models import Player
from django.utils import timezone
from datetime import timedelta
from user_app.serializers import PlayerRegisterSerializer, PlayerLoginSerializer, VerifyCodeSerializer, PlayerSerializer


# Класс для тестирования API, связанных с моделью Player
class PlayerAPITests(APITestCase):
    def setUp(self):
        # Данные для регистрации пользователя
        self.user_data = {
            'login': 'testuser',
            'email': 'testuser@example.com',
            'password': 'testpassword',
            'phone': '12345678901',
            'gender': 'M',
            'first_name': 'Test',
            'last_name': 'User'
        }
        # Данные для входа пользователя
        self.login_data = {
            'login': 'testuser',
            'password': 'testpassword'
        }
        # Данные для верификации кода
        self.verification_data = {
            'code': '123456'  # Пример кода верификации
        }

    # Тест на регистрацию пользователя
    def test_register_user(self):
        url = reverse('register')  # Получение URL для регистрации
        serializer = PlayerRegisterSerializer(data=self.user_data)  # Сериализация данных
        self.assertTrue(serializer.is_valid(), msg=serializer.errors)  # Проверка валидности данных
        response = self.client.post(url, serializer.validated_data, format='json')  # Отправка POST-запроса
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # Проверка статуса ответа
        self.assertEqual(Player.objects.count(), 1)  # Проверка количества созданных пользователей
        self.assertEqual(Player.objects.get().login, 'testuser')  # Проверка логина созданного пользователя
        self.assertFalse(Player.objects.get().is_active)  # Проверка, что аккаунт неактивен

    # Тест на вход пользователя
    def test_login_user(self):
        Player.objects.create_user(**self.user_data)  # Создание пользователя
        url = reverse('login')  # Получение URL для входа
        serializer = PlayerLoginSerializer(data=self.login_data)  # Сериализация данных
        self.assertTrue(serializer.is_valid())  # Проверка валидности данных
        response = self.client.post(url, serializer.validated_data, format='json')  # Отправка POST-запроса
        self.assertEqual(response.status_code,
                         status.HTTP_400_BAD_REQUEST)  # Проверка статуса ответа (аккаунт неактивен)

    # Тест на верификацию кода
    def test_verify_code(self):
        player = Player.objects.create_user(**self.user_data)  # Создание пользователя
        player.verification_code = '123456'  # Установка кода верификации
        player.code_expiry = timezone.now() + timedelta(minutes=5)  # Установка срока действия кода
        player.save()  # Сохранение пользователя
        url = reverse('verify')  # Получение URL для верификации
        serializer = VerifyCodeSerializer(data=self.verification_data)  # Сериализация данных
        self.assertTrue(serializer.is_valid())  # Проверка валидности данных
        response = self.client.post(url, serializer.validated_data, format='json')  # Отправка POST-запроса
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # Проверка статуса ответа
        player.refresh_from_db()  # Обновление данных пользователя из базы
        self.assertTrue(player.is_active)  # Проверка, что аккаунт активен

    # Тест на выход пользователя
    def test_logout_user(self):
        player = Player.objects.create_user(**self.user_data)  # Создание пользователя
        self.client.force_authenticate(user=player)  # Аутентификация пользователя
        url = reverse('logout')  # Получение URL для выхода
        response = self.client.post(url)  # Отправка POST-запроса
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # Проверка статуса ответа

    # Тест на обновление профиля пользователя
    def test_update_profile(self):
        player = Player.objects.create_user(**self.user_data)  # Создание пользователя
        self.client.force_authenticate(user=player)  # Аутентификация пользователя
        url = reverse('player')  # Получение URL для обновления профиля
        update_data = {'gender': 'F'}  # Данные для обновления
        serializer = PlayerSerializer(instance=player, data=update_data, partial=True)  # Сериализация данных
        self.assertTrue(serializer.is_valid())  # Проверка валидности данных
        response = self.client.put(url, serializer.validated_data, format='json')  # Отправка PUT-запроса
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # Проверка статуса ответа
        player.refresh_from_db()  # Обновление данных пользователя из базы
        self.assertEqual(player.gender, 'F')  # Проверка обновленного поля

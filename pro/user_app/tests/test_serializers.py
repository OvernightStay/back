from rest_framework.test import APITestCase
from ..models import Player
from ..serializers import PlayerRegisterSerializer, PlayerLoginSerializer, VerifyCodeSerializer, PlayerSerializer


class SerializerTests(APITestCase):
    def setUp(self):
        # Создание уникальных значений для полей, которые должны быть уникальными
        self.unique_suffix = self._testMethodName  # Используем имя теста для создания уникального суффикса
        self.user_data = {
            'login': f'testuser_{self.unique_suffix}',
            'email': f'testuser_{self.unique_suffix[:10]}@example.com',  # Ограничиваем длину email до 50 символов
            'password': 'testpassword',
            'phone': f'1234567890{self.unique_suffix[-1]}',  # Уникальный телефон
            'gender': 'M',
            'first_name': 'Test',
            'last_name': 'User'
        }
        self.login_data = {
            'login': f'testuser_{self.unique_suffix}',
            'password': 'testpassword'
        }
        self.verification_data = {
            'code': '123456'  # Пример кода верификации
        }
        # Создание пользователя для тестирования сериализатора PlayerSerializer
        self.player = Player.objects.create_user(**self.user_data)

    # Тест для PlayerRegisterSerializer
    def test_player_register_serializer(self):
        # Удаление существующего пользователя с таким же email
        Player.objects.filter(email=self.user_data['email']).delete()

        # Создание новых уникальных значений для полей, которые должны быть уникальными
        unique_suffix = f'{self._testMethodName}_new'
        new_user_data = {
            'login': f'testuser_{unique_suffix}',
            'email': f'testuser_{unique_suffix[:10]}@example.com',  # Ограничиваем длину email до 50 символов
            'password': 'testpassword',
            'phone': f'1234567890{unique_suffix[-1]}',  # Уникальный телефон, содержащий только цифры
            'first_name': 'Test',
            'last_name': 'User'
        }
        # Убедимся, что в поле phone передаются только цифры и их ровно 11
        new_user_data['phone'] = ''.join(filter(str.isdigit, new_user_data['phone']))
        if len(new_user_data['phone']) < 11:
            new_user_data['phone'] += '0' * (11 - len(new_user_data['phone']))
        elif len(new_user_data['phone']) > 11:
            new_user_data['phone'] = new_user_data['phone'][:11]

        serializer = PlayerRegisterSerializer(data=new_user_data)
        self.assertTrue(serializer.is_valid(), msg=serializer.errors)  # Проверка валидности данных
        player = serializer.save()
        self.assertEqual(player.login, new_user_data['login'])  # Проверка логина
        self.assertEqual(player.email, new_user_data['email'])  # Проверка email
        self.assertEqual(player.phone, new_user_data['phone'])  # Проверка телефона
        self.assertEqual(player.first_name, new_user_data['first_name'])  # Проверка имени
        self.assertEqual(player.last_name, new_user_data['last_name'])  # Проверка фамилии

    # Тест для PlayerLoginSerializer
    def test_player_login_serializer(self):
        serializer = PlayerLoginSerializer(data=self.login_data)
        self.assertTrue(serializer.is_valid(), msg=serializer.errors)  # Проверка валидности данных
        validated_data = serializer.validated_data
        self.assertEqual(validated_data['login'], self.login_data['login'])  # Проверка логина
        self.assertEqual(validated_data['password'], self.login_data['password'])  # Проверка пароля

    # Тест для VerifyCodeSerializer
    def test_verify_code_serializer(self):
        serializer = VerifyCodeSerializer(data=self.verification_data)
        self.assertTrue(serializer.is_valid(), msg=serializer.errors)  # Проверка валидности данных
        validated_data = serializer.validated_data
        self.assertEqual(validated_data['code'], self.verification_data['code'])  # Проверка кода

    # Тест для PlayerSerializer
    def test_player_serializer(self):
        serializer = PlayerSerializer(instance=self.player)
        self.assertEqual(serializer.data['login'], self.player.login)  # Проверка логина
        self.assertEqual(serializer.data['email'], self.player.email)  # Проверка email
        self.assertEqual(serializer.data['phone'], self.player.phone)  # Проверка телефона
        self.assertEqual(serializer.data['gender'], self.player.gender)  # Проверка пола
        self.assertEqual(serializer.data['first_name'], self.player.first_name)  # Проверка имени
        self.assertEqual(serializer.data['last_name'], self.player.last_name)  # Проверка фамилии

        # Тест на обновление данных
        update_data = {'gender': 'F'}
        serializer = PlayerSerializer(instance=self.player, data=update_data, partial=True)
        self.assertTrue(serializer.is_valid(), msg=serializer.errors)  # Проверка валидности данных
        serializer.save()
        self.player.refresh_from_db()
        self.assertEqual(self.player.gender, 'F')  # Проверка обновленного поля

# Getting Started
***
### Клонируйте репозиторий с GitHub и переключитесь на директорию проекта:
```commandline
git clone https://github.com/OvernightStay/back
```

### Создайте виртуальное окружение и активируйте его:
```commandline
python -m venv venv
venv\scripts\activate
```

### Установите необходимые для работы библиотеки:
```commandline
pip install -r ../requirements.txt
```

### Сделайте миграции:
```commandline
python manage.py makemigrations
python manage.py migrate
```

### Создайте файл .env в корневой папке и укажите свои переменные для почтовых отправлений:
```
EMAIL_HOST=''
EMAIL_PORT=
EMAIL_HOST_USER=''
EMAIL_HOST_PASSWORD=''
DEFAULT_FROM_EMAIL=''
```

### Запустите сервер:

```commandline
python manage.py runserver
```
---
# Использование

## Модели

## Регистрация и учётные данные игрока

### ```register/```
Регистрация.   
Запрашиваемые аргументы:
* ```email```
* ```phone```
* ```password```
* ```first_name```
* ```last_name```

### ```login/```
Аутентификация.   
Аргументы:
* ```login``` (email или phone)
* ```password```

### ```verify/```
Подтверждение аккаунта.   
Аргументы:
* ```code```

### ```logout/```
Выход из аккаунта. Не запрашивает аргументов.

### ```player/```
Просмотр и изменение информации игрока.   
Аргументы:
* ```first_name```
* ```last_name```
* ```phone```
* ```email```

### ```password-reset/```
Запрос на изменение пароля.   
Аргументы:
* ```email```

### ```password-reset-confirm/```
Подтверждение нового пароля.   
Аргументы:
* ```email```
* ```code```
* ```new_password```
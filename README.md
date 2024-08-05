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
pip install -r requirements.txt
```

### Создайте файл .env в корневой папке и укажите свои переменные для почтовых отправлений:
```
EMAIL_HOST=''
EMAIL_PORT=
EMAIL_HOST_USER=''
EMAIL_HOST_PASSWORD=''
DEFAULT_FROM_EMAIL=''
```

### Перейдите в основную папку проекта и сделайте миграции:
```commandline
cd pro
python manage.py makemigrations
python manage.py migrate
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
* ```login```
* ```password```
* ```email```
* ```phone```
* ```first_name```
* ```last_name```

### ```login/```
Аутентификация.   
Аргументы:
* ```login```
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
* ```gender```
* ```training_check```

### ```password-reset/```
Запрос на изменение пароля.   
Аргументы:
* ```email```

### ```password-reset-confirm/```
Подтверждение нового пароля.   
Аргументы:
* ```code```
* ```new_password```
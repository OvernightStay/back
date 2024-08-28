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

Поле ```email``` является не обязательным.  
Если он указывается, отправляется письмо с данными для авторизации.

### ```login/```
Аутентификация.   
Аргументы:
* ```login```
* ```password```

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
* ```current_password```
* ```new_password```    

Аргументы ```current_password``` и ```new_password``` используются при изменении пароля.    
Если введены оба - идёт проверка текущего, если только ```new_password```, пароль меняется.   
Первый метод будет использоваться при изменении пароля из настроек в личном кабинете;   
второй - при восстановлении через почту.

### ```password-reset/```
Запрос на восстановление пароля.   
Аргументы:
* ```email```

### ```password-reset-confirm/```
Подтверждение привязки аккаунта к почте.   
Аргументы:
* ```code```
# TEST_DRF_friend_service
## Запуск сервиса
1. Клонировать репозиторий:
```
git clone https://github.com/MikhailBogachev/TEST_DRF_friend_service.git
```
2. Gерейти в него в командной строке:
```
cd TEST_DRF_friend_service
```
### Запуск с помощью docker
3. Выполнить последовательно две команды:
```
docker build -t django_drf .
```

```
docker run -d -p 8080:8000 --name django_drf_app django_drf
```
### Запуск с помощью Python env
3. Cоздать и активировать виртуальное окружение:
```
python3 -m venv env
```

```
source env/bin/activate
```
4. Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

5. Выполнить миграции:

```
python3 manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver
```

## Примеры запросов. (Порт при запуске через dockerfile: 8080, через python env: 8000)
__**POST**__ Регистрация пользователя  
**URL**: http://127.0.0.1:8080/api/auth/users/  
**Body**:
```
{
  "username": "user2"
  "password": "user2pass1234"
}
```
**Response (JSON)**:
```
{
    "email": "",
    "username": "user2",
    "id": 2
}
```

__**POST**__ Получение токена  
**URL**: http://127.0.0.1:8080/api/auth/users/  
**Body**:
```
{
    "username": "user2",
    "password": "user2pass1234"
}
```
**Response (JSON)**:
```
{
    "auth_token": "f40fda302c9d0b170b3771122a9e8461..."
}
```

__При запросах на следующие эндпоинты передаем токен в Headers (Token f40fda302c9d0b170b3771122a9e8461...)__

__**GET**__ Получить список входящих/исходящих запросов в друзья  
**URL**: http://127.0.0.1:8080/api/friend-requests/  
**Response (JSON)**:
```
{
    "outgoing_requests": [
        {
            "id": 58,
            "from_user": "user2",
            "to_user": "user3",
            "accepted": false
        }
    ],
    "incoming_requests": [
        {
            "id": 56,
            "from_user": "user1",
            "to_user": "user2",
            "accepted": true
        }
    ]
}
```

__**POST**__ Отправить заявку в друзья другому пользователю  
**URL**: http://127.0.0.1:8080/api/friend-requests/  
**Body**:
```
{
    "to_user": "user1",
}
```
**Response (JSON)**:
```
{
    "outgoing_requests": [
        {
            "id": 1,
            "from_user": "user2",
            "to_user": "user3",
            "accepted": false
        }
    ],
    "incoming_requests": [
        {
            "id": 2,
            "from_user": "user1",
            "to_user": "user2",
            "accepted": false
        }
    ]
}
```

__**GET**__ **Принять** входящую заявку в друзья. id - id входящей заявки  
**URL**: http://127.0.0.1:8080/api/friend-requests/{id}/accept/ 
**Response (JSON)**:
```
{
    "status": "Заявка принята"
}
```


__**GET**__ **Отклонить** входящую заявку в друзья. id - id входящей заявки  
**URL**: http://127.0.0.1:8080/api/friend-requests/{id}/reject/ 
**Response (JSON)**:
```
{
    "status": "Заявка отклонена"
}
```

__**GET**__ Получить список друзей  
**URL**: http://127.0.0.1:8080/api/friends/  
**Response (JSON)**:
```
{
    "friends": [
        {
            "id_friendship": 12,
            "friend": "user1"
        }
    ]
}
```

__**GET**__ Получить статус дружбы с пользователем  
**URL**: http://127.0.0.1:8080/api/friends/{username}/  
**Response (JSON)**:
```
{
    "answer": "Уже друзья"
}
```

__**DELETE**__ Удалить пользователя из друзей  
**URL**: http://127.0.0.1:8080/api/friends/{username}/  
**Response (JSON)**:
```
{
    "status": "Пользователь удален из друзей"
}
```

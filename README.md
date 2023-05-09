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
### Запуск с помощью Python
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

### Описание проекта:

Проект YaMDb собирает отзывы пользователей на произведения. Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.
Произведения делятся на категории. Произведению может быть присвоен жанр из списка предустановленных. Пользователи могут оставлять к произведениям текстовые отзывы и ставить оценку произведению. Из пользовательских оценок формируется усреднённая оценка произведения — рейтинг. Пользователи могут оставлять комментарии к отзывам. 
В проекте реализован бэкенд и API для него.

### Исполнители:

Иван Дитятев https://github.com/ivditm

Евгений Панкрушев https://github.com/NetWorm32

Данила Мисиюк https://github.com/MisiyukDA

### Пререквизиты:

- macOS Monterey 12.3
- Python 3.9
- pip
- csv
- SQLite
- git

### Описание запуска проекта:
### Исполнители:

Иван Дитятев https://github.com/ivditm

Евгений Панкрушев https://github.com/NetWorm32

Данила Мисиюк https://github.com/MisiyukDA

### Пререквизиты:

- macOS Monterey 12.3
- Python 3.9
- pip
- csv
- SQLite
- git

### Описание запуска проекта:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:ivditm/api_yamdb.git
```

```
cd api_yamdb
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
```

```
source env/bin/activate
```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver
```

Импорт БД из csv:

```
python3 api_yamdb/managment/commands.py
```

### Тестирование:

Redoc:

```
http://127.0.0.1:8000/redoc
```

Получение списка всех категорий

```
GET http://127.0.0.1:8000/api/v1/categories/
```

Добавление новой категории

```
POST http://127.0.0.1:8000/api/v1/categories/

{
  "name": "string",
  "slug": "string"
}
```

Получение списка всех жанров

```
GET http://127.0.0.1:8000/api/v1/genres/
```

Добавление жанра

```
POST http://127.0.0.1:8000/api/v1/genres/

{
  "name": "string",
  "slug": "string"
}
```

Получение списка всех произведений

```
GET http://127.0.0.1:8000/api/v1/titles/
```

Добавление произведения

```
POST http://127.0.0.1:8000/api/v1/titles/

{
"name": "string",
"year": 0,
"description": "string",
"genre": [
"string"
],
"category": "string"
}
```

Получение информации о произведении

```
GET http://127.0.0.1:8000/api/v1/titles/{titles_id}/
```

Получение списка всех отзывов

```
GET http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/
```

Добавление нового отзыва

```
POST http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/

{
  "text": "string",
  "score": 1
}
```

Полуение отзыва по id

```
GET http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/
```

Получение списка всех комментариев к отзыву

```
GET http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/comments/
```

Добавление комментария к отзыву

```
POST http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/comments/

{
  "text": "string"
}
```

Получение комментария к отзыву

```
GET http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/
```

Получение данных своей учетной записи

```
GET http://127.0.0.1:8000/api/v1/users/me/
```

Изменение данных своей учетной записи

```
PATCH http://127.0.0.1:8000/api/v1/users/me/

{
  "username": "string",
  "email": "user@example.com",
  "first_name": "string",
  "last_name": "string",
  "bio": "string"
}
```

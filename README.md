# Шаблон асинхронного проекта на FastAPI

### Основные используемые библиотеки:
- SQLAlchemy (ORM);
- Redis (Cache);
- Loguru (Logging);
- Alembic (Migrations);
- Pydantic-settings (ENV variables);

## Что в шаблоне

### 1. Endpoints для авторизации `app/handlers/auth.py`:
- Регистрация пользователя - `/api/v1/auth/users`
- Получение JWT - `/api/v1/auth/token`
- Обновление access JWT - `/api/v1/auth/refresh`
- Получение своих данных - `/api/v1/auth/myself`

### 2. Модель пользователя с полями `app/models.py`:
- `id`
- `username`
- `first_name`
- `last_name`
- `email`
- `password`
- `date_join`
- `last_login`
- `is_superuser`
- `is_staff`
- `is_active`

### 3. Middleware для логирования `app/middlewares/logging.py`.

### 4. Cache (Redis, Local).

Для использования необходимо указать переменные окружения:

    REDIS_HOST
    REDIS_PASSWORD
    REDIS_PORT
    REDIS_DB

`app/services/cache/redis.py`

Иначе будет использоваться локальный кэш.

`app/services/cache/local.py`

### 5. Настройки проекта - `app/settings.py`.

Переменные окружения проекта

### 6. Возможность создать миграции через alembic:

В шаблоне ещё нет ни одной миграции, их нужно создать.

Для PostgreSQL необходимо добавить библиотеку `asyncpg`.

```shell
poetry add asyncpg;
export DATABASE_URL='postgresql+asyncpg://username:password@hostname/dbname';
alembic revision --autogenerate -m 'init';
alembic upgrade head;
``` 
Для MySQL и MariaDB необходимо добавить библиотеку `aiomysql`.
Также нужно указать переменную окружения `DATABASE_URL` для создания миграции в alembic.

```shell
poetry add aiomysql;
export DATABASE_URL='mysql+aiomysql://username:password@hostname/dbname?charset=utf8mb4';
alembic revision --autogenerate -m 'init';
alembic upgrade head;
``` 

Для SQLite необходимо добавить библиотеку `aiosqlite`.
Также нужно указать переменную окружения `DATABASE_URL` для создания миграции в alembic.

```shell
poetry add aiosqlite;
export DATABASE_URL='sqlite+aiosqlite:///sqlite.db';
alembic revision --autogenerate -m 'init';
alembic upgrade head;
```


## Запуск

Чтобы запустить проект с логгированием всех сообщений (даже старт сервера) в формате JSON, 
нужно запустить файл `run.py`

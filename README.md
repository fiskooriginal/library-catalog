# Library Catalog API

Бэкенд-сервис для управления библиотечным каталогом на FastAPI с использованием Clean Architecture.

## Описание

API для управления каталогом книг с поддержкой:

- CRUD операции для книг
- Фильтрация и поиск книг
- Пагинация результатов
- Интеграция с Open Library API для получения метаданных книг
- Поддержка нескольких хранилищ данных (PostgreSQL, JSONBinIO, файловая система)

## Технологический стек

- **Python** 3.13+
- **FastAPI** — современный веб-фреймворк
- **SQLAlchemy** — ORM для работы с базой данных
- **Alembic** — миграции базы данных
- **PostgreSQL** — основная база данных
- **uv** — быстрый менеджер пакетов Python
- **Docker** — контейнеризация приложения

## Архитектура проекта

Проект следует принципам Clean Architecture и разделен на слои:

```text
src/library_catalog/
├── domain/              # Доменный слой (бизнес-логика)
│   ├── entities/        # Сущности предметной области
│   ├── repositories/    # Интерфейсы репозиториев
│   ├── gateways/        # Интерфейсы внешних сервисов
│   ├── exceptions/      # Доменные исключения
│   └── vo/              # Value Objects
├── application/         # Слой приложения
│   ├── use_cases/       # Use cases (бизнес-сценарии)
│   ├── dtos/           # Data Transfer Objects
│   ├── mappers/        # Маппинг между слоями
│   └── uow/            # Unit of Work паттерн
├── infrastructure/      # Инфраструктурный слой
│   ├── persistence/     # Реализация репозиториев
│   ├── gateways/        # Реализация внешних сервисов
│   ├── http/            # HTTP клиенты
│   ├── config/          # Конфигурация
│   └── di/              # DI-factories
└── presentation/        # Слой представления
    └── api/             # REST API эндпоинты
        └── v1/          # API версия 1
```

## Требования

- **Python** 3.13+
- **uv** — менеджер пакетов ([репозиторий](https://github.com/astral-sh/uv))
- **PostgreSQL** 16+ (для работы с базой данных)

### Установка uv

**macOS/Linux:**

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Через pip:**

```bash
pip install uv
```

**macOS (Homebrew):**

```bash
brew install uv
```

## Быстрый старт

### 1. Установка зависимостей

```bash
uv sync
```

Команда создает виртуальное окружение и устанавливает все зависимости из `pyproject.toml`.

### 2. Настройка переменных окружения

Скопируйте файл с примерами переменных окружения:

```bash
cp .env.example .env
```

Отредактируйте `.env` файл при необходимости. Значения по умолчанию подходят для локальной разработки.

### 3. Настройка базы данных

Используйте значения из `.env` файла для создания базы данных.

### 4. Применение миграций

```bash
uv run alembic upgrade head
```

### 5. Запуск приложения

```bash
uv run uvicorn src.library_catalog.presentation.main:app --reload
```

### 6. Доступ к приложению

После запуска приложение будет доступно по следующим адресам:

- **API**: `http://127.0.0.1:8000`
- **Swagger UI**: `http://127.0.0.1:8000/docs`
- **ReDoc**: `http://127.0.0.1:8000/redoc`

## API Эндпоинты

Все API эндпоинты находятся под префиксом `/api/v1`.

### Книги

- `GET /api/v1/books` — получить список книг с фильтрацией и пагинацией
- `GET /api/v1/books/{uuid}` — получить книгу по UUID
- `POST /api/v1/books` — создать новую книгу
- `PUT /api/v1/books/{uuid}` — обновить книгу
- `DELETE /api/v1/books/{uuid}` — удалить книгу

## Запуск приложения

### Локальная разработка

Стандартный запуск с авто-перезагрузкой:

```bash
uv run uvicorn src.library_catalog.presentation.main:app --reload
```

Запуск на другом хосте/порту:

```bash
uv run uvicorn src.library_catalog.presentation.main:app \
    --host 0.0.0.0 \
    --port 8000 \
    --reload
```

Альтернативный способ (активация виртуального окружения):

```bash
source .venv/bin/activate
uvicorn src.library_catalog.presentation.main:app --reload
```

## Docker

Проект включает полную Docker-интеграцию с поддержкой production и development режимов.

### Требования для Docker

- **Docker** 20.10+
- **Docker Compose** 2.0+

### Быстрый старт с Docker

1. Скопируйте файл с переменными окружения:

   ```bash
   cp .env.example .env
   ```

2. При необходимости отредактируйте `.env` файл.

3. Запустите приложение:

   **Production режим:**

   ```bash
   docker-compose up -d
   ```

   **Development режим с hot-reload:**

   ```bash
   docker-compose -f docker-compose.yml -f docker-compose.dev.yml up
   ```

### Доступ к приложению

После запуска приложение будет доступно по тем же адресам:

- **API**: `http://127.0.0.1:8000`
- **Swagger UI**: `http://127.0.0.1:8000/docs`
- **ReDoc**: `http://127.0.0.1:8000/redoc`

### Управление контейнерами

**Просмотр логов:**

```bash
# Все сервисы
docker-compose logs -f

# Только приложение
docker-compose logs -f app

# Только база данных
docker-compose logs -f db
```

**Остановка контейнеров:**

```bash
docker-compose down
```

**Остановка с удалением volumes (удалит данные БД):**

```bash
docker-compose down -v
```

### Миграции базы данных

Миграции запускаются автоматически при старте контейнера через entrypoint скрипт.

**Ручной запуск миграций:**

```bash
docker-compose exec app uv run alembic upgrade head
```

**Создание новой миграции:**

```bash
docker-compose exec app uv run alembic revision --autogenerate -m "описание миграции"
```

### Переменные окружения для Docker

В Docker Compose переменные окружения задаются через `.env` файл. Основные настройки:

- **DB_HOST** — хост базы данных (в Docker используйте `db`)
- **DB_PORT** — порт базы данных (по умолчанию `5432`)
- **DB_NAME** — имя базы данных (по умолчанию `library_catalog`)
- **DB_USER** — пользователь БД (по умолчанию `postgres`)
- **DB_PASSWORD** — пароль БД (по умолчанию `postgres`)

Полный список переменных окружения см. в файле `.env.example`.

### Troubleshooting

**Проблема**: Контейнер приложения не запускается

- Проверьте логи: `docker-compose logs app`
- Убедитесь, что база данных готова: `docker-compose logs db`
- Проверьте переменные окружения в `.env` файле

**Проблема**: Ошибки подключения к базе данных

- Убедитесь, что `DB_HOST=db` в переменных окружения
- Проверьте, что сервис `db` запущен: `docker-compose ps`
- Проверьте healthcheck базы данных: `docker-compose ps db`

**Проблема**: Миграции не применяются

- Проверьте логи entrypoint скрипта: `docker-compose logs app | grep migration`
- Запустите миграции вручную: `docker-compose exec app uv run alembic upgrade head`

## Работа с миграциями

### Применение миграций

```bash
uv run alembic upgrade head
```

### Создание новой миграции

```bash
uv run alembic revision --autogenerate -m "описание изменений"
```

### Откат миграции

```bash
uv run alembic downgrade -1
```

## Переменные окружения

Все переменные окружения описаны в файле `.env.example`. Основные категории:

### База данных

- `DB_HOST` — хост PostgreSQL (по умолчанию: `localhost`)
- `DB_PORT` — порт PostgreSQL (по умолчанию: `5432`)
- `DB_NAME` — имя базы данных (по умолчанию: `library_catalog`)
- `DB_USER` — пользователь БД (по умолчанию: `postgres`)
- `DB_PASSWORD` — пароль БД (по умолчанию: `postgres`)

### Open Library API

- `OPEN_LIBRARY_BASE_URL` — базовый URL Open Library API
- `OPEN_LIBRARY_SEARCH_PATH` — путь для поиска
- `OPEN_LIBRARY_REQUEST_TIMEOUT_SECONDS` — таймаут запросов
- `OPEN_LIBRARY_SEARCH_LIMIT` — лимит результатов поиска

### Хранилище файлов

- `JSON_FILE_PATH` — путь к JSON файлу для хранения (для aiofiles репозитория)

### JSONBin.io

- `JSONBIN_API_KEY` — API ключ для JSONBin.io
- `JSONBIN_BIN_ID` — ID бина для хранения данных

## Разработка

### Структура проекта

Проект следует принципам Clean Architecture:

- **Domain** — чистая бизнес-логика, не зависит от внешних библиотек
- **Application** — use cases и бизнес-сценарии
- **Infrastructure** — реализация технических деталей (БД, HTTP клиенты)
- **Presentation** — API эндпоинты и схемы валидации

### Зависимости

Зависимости управляются через `uv` и `pyproject.toml`:

- **Основные зависимости** — установлены для всех окружений
- **dev** — инструменты разработки (pre-commit)
- **lint** — инструменты линтинга (ruff)
- **test** — инструменты тестирования (pytest)

### Pre-commit

В проекте настроен [pre-commit](https://pre-commit.com/) для автоматической проверки и форматирования кода перед коммитами.

**Установка хуков:**

```bash
uv run pre-commit install
```

**Что запускается автоматически:**

- **ruff** — линтинг и автоисправления
- **ruff-format** — форматирование кода

**Ручной запуск проверок:**

```bash
# Все файлы
uv run pre-commit run --all-files

# Конкретные файлы
uv run pre-commit run --files path/to/file.py
```

**Обновление версий хуков:**

```bash
uv run pre-commit autoupdate
```

### Линтинг и форматирование

Проект использует **ruff** для линтинга и форматирования кода.

**Запуск линтинга:**

```bash
uv run ruff check .
```

**Автоисправление:**

```bash
uv run ruff check --fix .
```

**Форматирование:**

```bash
uv run ruff format .
```

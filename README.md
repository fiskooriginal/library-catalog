# Library Backend

Бэкенд для библиотечного каталога на FastAPI.

## Быстрый старт

```bash
# 1) Установите зависимости
uv sync

# 2) Запустите приложение в dev-режиме
uv run uvicorn src.main:app --reload

# 3) Откройте в браузере
# API:    http://127.0.0.1:8000
# Swagger http://127.0.0.1:8000/docs
# ReDoc   http://127.0.0.1:8000/redoc
```

## Требования

- **Python** 3.13+
- **uv** — быстрый менеджер пакетов для Python ([репозиторий](https://github.com/astral-sh/uv))

### Установка uv

- Скрипт установки:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

- Через pip:

```bash
pip install uv
```

- Через Homebrew (macOS):

```bash
brew install uv
```

## Установка зависимостей

```bash
uv sync
```

- Создает виртуальное окружение (если его еще нет)
- Устанавливает зависимости из `pyproject.toml`
- Использует `uv.lock` для воспроизводимости

## Запуск приложения

Стандартный запуск с авто-перезагрузкой:

```bash
uv run uvicorn src.main:app --reload
```

Запуск на другом хосте/ порту:

```bash
uv run uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
```

Альтернатива: активировать виртуальное окружение и запускать напрямую:

```bash
source .venv/bin/activate
uvicorn src.main:app --reload
```

### Доступ к приложению

- **API**: `http://127.0.0.1:8000`
- **Swagger UI**: `http://127.0.0.1:8000/docs`
- **ReDoc**: `http://127.0.0.1:8000/redoc`

## Pre-commit

В проекте настроен [pre-commit](https://pre-commit.com/) для автоматической проверки и форматирования кода перед коммитами.

### Установка хуков

После `uv sync` хуки обычно устанавливаются автоматически. Если нужно установить вручную:

```bash
uv run pre-commit install
```

### Что запускается автоматически

- **ruff** — линтинг и автоисправления
- **ruff-format** — форматирование кода

Если проверки не прошли, коммит будет отклонен. После исправлений повторите попытку.

### Ручной запуск проверок

Проверить все файлы:

```bash
uv run pre-commit run --all-files
```

Проверить конкретные файлы:

```bash
uv run pre-commit run --files path/to/file.py
```

### Обновление версий хуков

```bash
uv run pre-commit autoupdate
```

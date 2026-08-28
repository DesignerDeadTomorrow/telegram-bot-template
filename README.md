# 👁️‍🗨️ telegram-bot-template

[![Python](https://img.shields.io/badge/Python-3.12%2B-orange?style=for-the-badge&logo=python&logoColor=white&labelColor=black)](https://www.python.org/downloads/release/python-3120/)
[![Aiogram](https://img.shields.io/badge/Aiogram-3.x-blueviolet?style=for-the-badge&logo=telegram&logoColor=blue&labelColor=black)](https://github.com/aiogram/aiogram)
[![Dishka](https://img.shields.io/badge/Dishka-DI-blue?style=for-the-badge&logo=pypy&logoColor=lightgrey&labelColor=black)](https://github.com/reagento/dishka)
[![Redis](https://img.shields.io/badge/Redis-async-red?style=for-the-badge&logo=redis&logoColor=red&labelColor=black)](https://github.com/redis/redis)

[![SQLalchemy](https://img.shields.io/badge/SQLalchemy-2.0-blue?style=for-the-badge&logo=postgresql&logoColor=white&labelColor=black)](https://github.com/sqlalchemy/sqlalchemy)
[![Alembic](https://img.shields.io/badge/Alembic-async-cyan?style=for-the-badge&logo=pandas&logoColor=blue&labelColor=black)](https://github.com/sqlalchemy/alembic)
[![Taskiq](https://img.shields.io/badge/Taskiq-tasks-red?style=for-the-badge&logo=PyTorch&logoColor=red&labelColor=black)](https://github.com/taskiq-python/taskiq)

[![Static Badge](https://img.shields.io/badge/Docker-Enabled-black?style=for-the-badge&logo=docker&logoColor=cyan&labelColor=black)](https://docs.docker.com/)
[![Ruff](https://img.shields.io/badge/Ruff-formatted-black?style=for-the-badge&logo=ruff&logoColor=yellowgreen&labelColor=black)](https://github.com/astral-sh/ruff)

---

## ⚡ Быстрый старт

### 1. Подготовка


**Для Windows (PowerShell)**
```bash
git clone https://github.com/DesignerDeadTomorrow/telegram-bot-template.git .

Copy-Item .env.example .env

python -m venv .venv
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\.venv\Scripts\Activate.ps1

pip install -r requirements.txt
```

**Для Windows (Bash)**
```bash
git clone https://github.com/DesignerDeadTomorrow/telegram-bot-template.git .

cp .env.example .env

python -m venv .venv
source .venv/Scripts/activate

pip install -r requirements.txt
```

**Для Linux/MacOS**
```bash
git clone https://github.com/DesignerDeadTomorrow/telegram-bot-template.git .

cp .env.example .env

python -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
```

### 2. Запуск через Docker
```bash
docker compose up -d --build
```

### 3. Локальный запуск
```bash
alembic upgrade head

python -m src.app.bot
```

### 4. Миграция Alembic

Создание авто-миграции
```bash
alembic revision --autogenerate -m "описание"
```

Миграция БД
```bash
alembic upgrade head
```

Откат последней миграции
```bash
alembic downgrade -1
```

---

## 💻 Технический Стек

* **Ядро:** Python 3.12, Aiogram 3.x
* **Внедрение зависимостей:** Dishka
* **База данных:** PostgreSQL, AsyncPG, SQlalchemy 2.0
* **Очередь задач:** Taskiq + Redis
* **Конфиг:** Pydantic Settings
* **Контейнеры:** Docker, Docker Compose

---

## 🪐 Особенности

* **Clean architecture**
* **Автоматическое управление ресурсами**
* **Graceful shutdown**
* **Готовые клиенты под 90% задач**

---

## ❔ Как работать

* **Код пишется в entities/ и modules/**
* **Если не нужна админка -- Удалить core/filters/role.py**
* **В entities/ пишутся сущности (models.py, schemas.py/dto.py, enums.py, repository.py)**
* **В modules/ пишутся фичи (handlers/, inline.py/reply.py, states.py, service.py, utils.py)**
* **ui/ используется для создание keyboards, и навигации по меню бота**

---

## 🏗️ Архитектура

```bash
├── migration # Настройки Alembic
│ ├── README
│ ├── env.py # Конфиг миграции
│ └── script.py.mako
│
├── src/ #Основной код
│ └── app/ # Точка входа
│ │ ├── bot.py # Точка входа бота
│ │ └── di.py # Создание контейнера с конфигом
│
│ └── core/ # Сердце проекта
│ │ └── filters/ # фильтры Aiogram
│ │ │ ├── init.py
│ │ │ ├── chat_type.py # Тип чата
│ │ │ └── role.py # Роли
│ │ └── middleware/ # Мидлвейры
│ │ │ ├── init.py
│ │ │ ├── callback_answer.py # Авто сброс загрузки у кнопок
│ │ │ └── throttling.py # Анти-спам
│ │ ├── init.py
│ │ ├── constants.py # Константы
│ │ └── exceptions.py # Кастомные ошибки
│
│ └── entities/ # Сущности
│   └── init.py
│
│ └── infrastructure/ # Инфраструктура
│ │ └── database/ # База данных
│ │ │ ├── init.py
│ │ │ ├── base.py # Шаблоны и модель таблицы
│ │ │ ├── client.py # Клиент
│ │ │ └── provider.py # DI
│ │ └── redis/ # Редис
│ │ │ ├── init.py
│ │ │ ├── client # Клиент
│ │ │ └── provider.py # DI
│ │ ├── init.py
│ │ ├── broker.py # Настройки Taskiq
│ │ └── config.py # Конфиги из .env данных
│
│ └── modules/ # Модули
│   └── init.py # Роутер
│
│ └─ ui/ # Клавиатуры, кнопки и навигация
│ │ ├── init.py
│ │ ├── builders.py # Генераторы клавиатур
│ │ ├── buttons.py # Отдельные кнопки назад
│ │ └── callbacks.py # Меню навигации
│
.env.example # Шаблон .env
README.md # Документация
alebmic.ini # Конфиг Alembic
docker-compose.yml # Сборщик контейнеров
dockerfile # Контейнер запуска
requirements.txt # Зависимости
```

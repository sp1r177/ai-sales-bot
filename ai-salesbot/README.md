# AI SalesBot — VK Mini App + FastAPI (Monorepo)

AI SalesBot — минимально жизнеспособный продукт для симуляции продаж с торгом. Фронтенд — VK Mini App (React + VKUI), бэкенд — FastAPI + PostgreSQL + Alembic. Запускается в Docker на Ubuntu.

## Архитектура

```
ai-salesbot/
  client/          # VK Mini App (React + VKUI)
  backend/         # FastAPI + PostgreSQL + Alembic
  docker/          # Dockerfile'ы и nginx конфиг
  docker-compose.yml
  .env.example
  README.md
  LICENSE
```

- Язык: TypeScript (client), Python 3.11 (backend)
- БД: PostgreSQL + SQLAlchemy 2.x + Alembic
- Авторизация: JWT (access/refresh)
- CORS: настраивается через `.env`
- Сборка: Docker + docker-compose
- Линтинг: ruff (py), eslint + prettier (ts)

## Требования
- Docker, Docker Compose
- Ubuntu 22.04+

## Установка и запуск

```bash
git clone <repo>
cd ai-salesbot
cp .env.example .env
# отредактируйте .env (DB, JWT, LLM, VITE_API_BASE)
docker compose up -d --build
```

После старта примените миграции БД:

```bash
docker compose exec backend alembic upgrade head
```

Бэкенд также создаёт таблицы на старте (MVP), но для совместимости и будущих апдейтов используйте Alembic.

## Доступы
- Backend API: `http://localhost:8000/api/v1`
- Frontend (через nginx): `http://localhost:8080`

## Эндпоинты (v1)
- POST `/auth/login` — вход по `vk_user_id` (MVP)
- POST `/auth/refresh`
- GET `/bots` — список ботов
- POST `/bots` — создать бота
- GET `/bots/{id}` — получить бота
- PUT `/bots/{id}` — обновить бота
- DELETE `/bots/{id}` — удалить бота
- POST `/uploads/image` — multipart upload (сохраняет в `backend/media/`)
- POST `/dialogs/start` — создать диалог
- POST `/dialogs/{id}/message` — отправить сообщение; бот отвечает через LLM
- GET `/dialogs/{id}` — лента сообщений
- GET `/analytics/overview` — метрики
- POST `/billing/subscribe?plan=free|start|pro|premium` — заглушка смены тарифа

## VK Mini App
- Укажите `VK_APP_ID` в `.env` (используется на фронте при необходимости)
- Подключен `vk-bridge`; получение `user_id` в экране Login через `VKWebAppGetUserInfo`

## LLM-провайдер
- Переключение: `LLM_PROVIDER=gigachat|yandexgpt`
- Вставьте реальные API URL и поля:
  - В `.env`: `LLM_API_URL=<ИЗ ОФИЦИАЛЬНОЙ ДОКУМЕНТАЦИИ>`
  - В коде провайдеров: `backend/app/services/llm/gigachat.py`, `backend/app/services/llm/yandexgpt.py`
- Формат ожидаемого запроса (MVP): `POST` JSON `{ model, messages, temperature, max_tokens }` с заголовком `Authorization: Bearer <LLM_API_KEY>`.
- Формат ответа: извлекается `choices[0].message.content` или `text`. При необходимости измените парсинг под реалии API.
- Логирование запросов: сообщения LLM помечаются `is_llm=true` в таблице `messages`.

## CORS
- Разрешённые домены задаются в `.env` переменной `BACKEND_CORS_ORIGINS` (через запятую), по умолчанию: `http://localhost:5173,https://vk.com`.

## Продакшен-деплой (пример)

```bash
sudo apt update && sudo apt install -y docker.io docker-compose-plugin
sudo usermod -aG docker $USER && newgrp docker
git clone <repo> && cd ai-salesbot
cp .env.example .env && nano .env
docker compose up -d --build
docker compose exec backend alembic upgrade head
```

## Медиа-файлы
- Загружаются локально в `backend/media/`
- Доступны по URL `/api/media/<filename>`
- Интерфейс хранения позволяет заменить на S3 в будущем

## Тарифы/оплата
- Эндпоинт подписки — заглушка: `/api/v1/billing/subscribe`
- Интеграция VK Pay/Stars/CryptoBot — TODO

## Планы развития
- Подпись запросов VK, валидация
- S3-хранилище
- Антиспам/лимиты по частоте
- Очередь фоновых задач

## Тесты

```bash
docker compose exec backend pytest -q
```

## Примечание по LLM URL
- В коде нет выдуманных URL. Укажите реальные конечные точки и поля в `.env` и провайдерах согласно официальной документации GigaChat / YandexGPT.
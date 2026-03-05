# Email Bot

Пет-проект: Telegram-бот для мониторинга почты через IMAP с уведомлениями о новых письмах.

## Идея

Проект решает простую задачу: добавить email в Telegram-боте и получать уведомления, когда в ящике появляются новые непрочитанные письма.

## Что внутри

- `telegram_bot` (Aiogram 3): диалог с пользователем, добавление/просмотр почт.
- `bot_backend` (Django + DRF): API для пользователей и email-аккаунтов.
- `celery` + `celery-beat`: периодическая проверка почты и отправка уведомлений.
- `postgres`: хранение пользователей и почтовых аккаунтов.
- `redis`: брокер Celery и FSM-хранилище бота.
- `nginx`: прокси к Django и раздача статики.

## Стек

- Python 3.13
- Aiogram 3
- Django 5 + DRF
- Celery
- PostgreSQL
- Redis
- Docker + Docker Compose

## Архитектура

1. Пользователь пишет `/start` боту.
2. Бот создает пользователя в backend (если его нет).
3. Пользователь добавляет email + пароль.
4. Backend проверяет IMAP-логин, шифрует пароль (Fernet), сохраняет в БД.
5. `celery-beat` по расписанию запускает проверку почтовых ящиков.
6. При новых письмах отправляется сообщение в Telegram.

## API (кратко)

- `POST /api/user/` - создать пользователя
- `GET /api/user/<tg_id>/` - получить пользователя
- `GET /api/user/<tg_id>/email/` - список почт пользователя
- `POST /api/user/<tg_id>/email/` - добавить почту
- `DELETE /api/user/<tg_id>/email/<email>/` - удалить почту

## Быстрый старт (Docker)

### 1. Подготовка `.env`

Скопировать шаблон:

```bash
cp .env-dev .env
```

Заполни обязательные поля в `.env`:

- `BOT_TOKEN`
- `BACKEND_URL` (для docker-сети удобно `http://nginx` или `http://backend:8000`, в зависимости от маршрутизации)
- `SECRET_KEY`
- `ALLOWED_HOSTS` (в текущей реализации значения разделяются пробелом, например: `localhost 127.0.0.1`)
- `FERNET_KEY`
- `POSTGRES_USER`
- `POSTGRES_PASSWORD`
- `REDIS_USER`
- `REDIS_PASSWORD`

Сгенерировать `FERNET_KEY` можно так:

```bash
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

### 2. Собрать образы

```bash
./build_images
```

### 3. Запустить сервисы

```bash
docker compose up -d
```

### 4. Проверка

- API: `http://localhost:1337/api/`
- Django admin: `http://localhost:1337/admin/`

Логи:

```bash
docker compose logs -f backend telegram_bot celery celery-beat
```

Остановка:

```bash
docker compose down
```

## Структура проекта

```text
src/
  telegram_bot/      # Aiogram бот
  bot_backend/       # Django API + Celery
nginx/               # reverse proxy config
docker-compose.yml
build_images
```
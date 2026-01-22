# Stage5
## Запуск приложения:
docker-compose up --build

## Команды для наполнения базы данных:
Для наполнения базы данных выполните последовательно следующие команды:
- Создайте суперпользователя командой "python manage.py create_superuser"
- Создайте пользователя командой "python manage.py createuser"
- Создайте объекты платежа (курс и урок) командой "python manage.py createstudy"
- Создайте платеж наличными за курс: "python manage.py createpaymentcoursecash"
- Создайте платеж безналичными за урок: "python manage.py createpaymentlessononline"
- Создайте группу Moderator "python manage.py create_moderatorgroup"
- Создайте пользователя и добавьте его в группу модераторов командой "python manage.py create_moderatoruser"


### Функционал
Подключена функция оплаты через stripe

### Запуск локально

 - Запустить Docker
 - Выполнить команду docker compose up --build (можно добавить флаг -d для запуска в фоновом режиме)

### GitHub Actions Workflow

#### Триггеры:
- **При push в любую ветку** (кроме develop) → запускаются только тесты
- **При pull request в ветку develop** → запускаются тесты + автоматический деплой

#### Jobs:
1. **test** - запуск тестов с PostgreSQL и Redis
2. **deploy** - автоматический деплой на сервер (только после успешных тестов)

#### Переменные окружения (Secrets) в GitHub:
Настройте в Settings → Secrets and variables → Actions:
- `SSH_KEY` - приватный SSH ключ для доступа к серверу
- `DEPLOY_SSH_KEY` - приватный SSH ключ для доступа к GitHub из сервера
- `SSH_USER` - пользователь на сервере
- `SERVER_IP` - IP адрес сервера
- `DEPLOY_DIR` - путь к проекту на сервере
- `DJANGO_SECRET_KEY` - секретный ключ Django
- `POSTGRES_USER` - пользователь PostgreSQL
- `POSTGRES_PASSWORD` - пароль PostgreSQL

### Документация
http://localhost:8000/swagger/ для Swagger UI 
http://localhost:8000/redoc/ для Redoc.

#### Тестирование
Реализованы тесты для CRUD Lesson

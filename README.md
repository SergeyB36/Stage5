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

### Отложенные задачи

Запуск celery и worker (на Windows):
celery -A config worker -l INFO --pool=eventlet


Запуск celery-beat в отдельном терминале (на Windows):
celery -A config beat --loglevel=info --scheduler django_celery_beat.schedulers:DatabaseScheduler


### Документация
http://localhost:8000/swagger/ для Swagger UI 
http://localhost:8000/redoc/ для Redoc.


#### Тестирование
Реализованы тесты для CRUD Lesson

##### Добавлен workflow
test 
add 
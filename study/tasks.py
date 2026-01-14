from celery import shared_task
from django.core.mail import send_mail

from config.settings import EMAIL_HOST_USER


# @shared_task
# def block_user(user):
#     """Функция блокировки пользователя"""
#     user.is_active = False
#     user.save()

@shared_task
def send_info_about_update(email:list, course_id: int):
    """Функция информирования подписчиков об обновлении курса"""
    from study.models import Course
    course = Course.objects.get(id=course_id)
    message = f'Курс {course.name} обновился!'
    send_mail("Обновление курса", message=message, from_email=EMAIL_HOST_USER,recipient_list=email)
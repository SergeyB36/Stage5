from datetime import timedelta

from celery import shared_task
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.utils import timezone

from config.settings import EMAIL_HOST_USER


@shared_task
def send_info_about_update(email: list, course_id: int):
    """Функция информирования подписчиков об обновлении курса"""
    from study.models import Course

    course = Course.objects.get(id=course_id)
    message = f"Курс {course.name} обновился!"
    send_mail("Обновление курса", message=message, from_email=EMAIL_HOST_USER, recipient_list=email)

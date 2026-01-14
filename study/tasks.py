from datetime import timedelta

from celery import shared_task
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.utils import timezone

from config.settings import EMAIL_HOST_USER


@shared_task
def block_user():
    """Функция блокировки пользователя"""
    User = get_user_model()
    three_months_ago = timezone.now() - timedelta(days=90)
    User.objects.filter(last_login__lt=three_months_ago, is_active=True).update(is_active=False)


@shared_task
def send_info_about_update(email: list, course_id: int):
    """Функция информирования подписчиков об обновлении курса"""
    from study.models import Course

    course = Course.objects.get(id=course_id)
    message = f"Курс {course.name} обновился!"
    send_mail("Обновление курса", message=message, from_email=EMAIL_HOST_USER, recipient_list=email)

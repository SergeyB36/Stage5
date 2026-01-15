from datetime import timedelta

from celery import shared_task
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.utils import timezone


@shared_task
def block_user():
    """Функция блокировки пользователя"""
    User = get_user_model()
    three_months_ago = timezone.now() - timedelta(days=90)
    User.objects.filter(last_login__lt=three_months_ago, is_active=True).update(is_active=False)

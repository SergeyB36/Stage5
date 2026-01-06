from django.core.management.base import BaseCommand
from django.utils import timezone

from study.models import Course
from users.models import CustomUser, Payments


class Command(BaseCommand):

    def handle(self, *args, **options):
        course = Course.objects.get(name="Кройка и шитье")
        user = CustomUser.objects.get(email="user@user.com")
        payment = Payments.objects.create(
            user=user,
            payment_date=timezone.now(),
            amount=2000,
            object_payment="course",
            type_payment="cash",
            course=course,
        )
        payment.save()
        print(f"Платеж {payment} успешно создан")

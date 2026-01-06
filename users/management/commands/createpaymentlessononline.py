from django.core.management.base import BaseCommand
from django.utils import timezone

from users.models import Payments, CustomUser
from study.models import Lesson

class Command(BaseCommand):

    def handle(self, *args, **options):
        lesson = Lesson.objects.get(name="Иголка")
        user = CustomUser.objects.get(email="user@user.com")
        payment = Payments.objects.create(
            user=user,
            payment_date=timezone.now(),
            amount=2000,
            object_payment="lesson",
            type_payment="on_line",
            lesson=lesson
        )
        payment.save()
        print(f"Платеж {payment} успешно создан")

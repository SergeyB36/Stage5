from django.core.management.base import BaseCommand

from users.models import CustomUser


class Command(BaseCommand):

    def handle(self, *args, **options):
        user = CustomUser.objects.create(email="admin@user.com")
        user.set_password("1234")
        user.is_staff = True
        user.is_superuser = True
        user.save()
        print(f"Пользователь {user} с правами superuser успешно создан")
        print(f"Login: '{user}'\nPassword: '1234'")

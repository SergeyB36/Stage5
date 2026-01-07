from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        group, group_created = Group.objects.get_or_create(name="Moderator")
        if group_created:
            return self.stdout.write(self.style.WARNING("Сначала создайте группу командой create_moderatorgroup"))

        User = get_user_model()

        user, user_created = User.objects.get_or_create(
            email="moderator@user.com",
        )
        if user_created:
            user.set_password("1234")
            user.is_active = True
            user.save()
            self.stdout.write(self.style.SUCCESS("Пользователь с правами модератора успешно создан"))

        user.groups.add(group)
        user.save()

        self.stdout.write(self.style.SUCCESS(f'Пользователь "{user}" успешно добавлен в группу "{group}"'))

from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand

from study.models import Course, Lesson


class Command(BaseCommand):
    help = 'Создает группу модераторов с необходимыми правами'

    def handle(self, *args, **options):
        group_name = "Moderator"
        group, created = Group.objects.get_or_create(name=group_name)

        course_content_type = ContentType.objects.get_for_model(Course)
        lesson_content_type = ContentType.objects.get_for_model(Lesson)

        permissions = Permission.objects.filter(
            content_type__in=[course_content_type, lesson_content_type],
            codename__in=[
                'view_course', 'change_course',
                'view_lesson', 'change_lesson',
            ]
        )

        group.permissions.set(permissions)

        if created:
            self.stdout.write(
                self.style.SUCCESS(f'Группа "{group_name}" успешно создана')
            )
        else:
            self.stdout.write(
                self.style.WARNING(f'Группа "{group_name}" уже существует, права обновлены')
            )

        self.stdout.write(
            self.style.SUCCESS(
                f'Назначенные права: {list(group.permissions.values_list("codename", flat=True))}'
            )
        )
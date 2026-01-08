from django.core.management.base import BaseCommand

from study.models import Course, Lesson


class Command(BaseCommand):

    def handle(self, *args, **options):
        course = Course.objects.create(name="Кройка и шитье", description="Курс кройки и шитья")
        course.save()
        self.stdout.write(self.style.SUCCESS(f"Курс '{course}' успешно создан"))
        lesson = Lesson.objects.create(
            name="Иголка", description="Иголка. Основные параметры, методы и функции", course=course
        )
        lesson.save()
        self.stdout.write(self.style.SUCCESS(f"К курсу '{course} 'успешно добавлен урок '{lesson}'"))

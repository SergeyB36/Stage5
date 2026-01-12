import json

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from study.models import Course, Lesson
from users.models import Subscription

User = get_user_model()


class LessonCRUDTestCase(APITestCase):
    """Тестирование CRUD операций для уроков"""

    def setUp(self):
        """Настройка тестовых данных"""
        # Создание модератора
        self.moderator = User.objects.create(email="moderator@test.com")
        self.moderator.set_password("123")
        self.is_staff = True
        self.group_name = "Moderator"
        self.group = Group.objects.create(name="Moderator")
        course_content_type = ContentType.objects.get_for_model(Course)
        lesson_content_type = ContentType.objects.get_for_model(Lesson)
        permissions = Permission.objects.filter(
            content_type__in=[course_content_type, lesson_content_type],
            codename__in=[
                "view_course",
                "change_course",
                "view_lesson",
                "change_lesson",
            ],
        )
        self.group.permissions.set(permissions)
        self.moderator.groups.add(self.group)
        self.moderator.save()

        # Создание владельца курса и уроков
        self.teacher = User.objects.create(email="teacher@test.com")
        self.teacher.set_password("123")
        self.teacher.save()

        # Создание студента - подписчика курса или уроков
        self.student = User.objects.create(email="student@test.com")
        self.student.set_password("123")
        self.student.save()

        # Создание курсов
        # Создание курса учителем
        self.course1 = Course.objects.create(
            name="Python для начинающих", description="Базовый курс Python", owner=self.teacher
        )

        self.course2 = Course.objects.create(
            name="Django разработка", description="Курс по Django фреймворку", owner=self.teacher
        )

        # Создание уроков учителем
        self.lesson1 = Lesson.objects.create(
            name="Введение в Python",
            description="Основы языка Python",
            course=self.course1,
            owner=self.teacher,
            url="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        )

        self.lesson2 = Lesson.objects.create(
            name="Установка Django",
            description="Как установить Django",
            course=self.course1,
            owner=self.teacher,
            url="https://www.youtube.com/watch?v=test123",
        )

    def test_create_lesson_by_teacher(self):
        """Тест создания урока преподавателем (владельцем курса)"""
        self.client.force_authenticate(user=self.teacher)

        data = {
            "name": "Новый урок",
            "description": "Описание нового урока",
            "course": self.course1.id,
            "url": "https://www.youtube.com/watch?v=test456",
        }

        response = self.client.post(reverse("study:lesson-create"), data=data, content_type="application/json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.last().name, "Новый урок")
        self.assertEqual(Lesson.objects.last().owner, self.teacher)

    def test_create_lesson_by_moderator(self):
        """Тест создания урока модератором"""
        self.client.force_authenticate(user=self.moderator)

        data = {
            "name": "Урок от модератора",
            "description": "Модератор создает урок",
            "course": self.course1.id,
            "url": "https://www.youtube.com/watch?v=moderator",
        }

        response = self.client.post(
            reverse("study:lesson-create"), data=json.dumps(data), content_type="application/json"
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Lesson.objects.count(), 2)

    def test_create_lesson_without_url(self):
        """Тест создания урока без URL"""
        self.client.force_authenticate(user=self.teacher)

        data = {"name": "Урок без видео", "description": "Урок без ссылки на видео", "course": self.course1.id}

        response = self.client.post(
            reverse("study:lesson-create"), data=json.dumps(data), content_type="application/json"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.count(), 3)

    def test_list_lessons(self):
        """Тест получения списка уроков (доступно всем)"""
        # Тестирование без аутентификации
        response = self.client.get(reverse("study:lesson-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Тестирование с аутентификацией
        self.client.force_authenticate(user=self.student)
        response = self.client.get(reverse("study:lesson-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Проверка пагинации
        self.assertIn("results", response.data)
        self.assertEqual(len(response.data["results"]), 2)

    def test_retrieve_lesson(self):
        """Тест получения деталей урока (доступно всем)"""
        # Без аутентификации
        response = self.client.get(reverse("study:lesson-retrieve", args=[self.lesson1.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Введение в Python")

        # С аутентификацией
        self.client.force_authenticate(user=self.student)
        response = self.client.get(reverse("study:lesson-retrieve", args=[self.lesson1.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_lesson_by_owner(self):
        """Тест обновления урока владельцем"""
        self.client.force_authenticate(user=self.teacher)

        data = {"name": "Обновленное название", "description": "Обновленное описание"}

        response = self.client.patch(
            reverse("study:lesson-update", args=[self.lesson1.id]),
            data=json.dumps(data),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.lesson1.refresh_from_db()
        self.assertEqual(self.lesson1.name, "Обновленное название")
        self.assertEqual(self.lesson1.description, "Обновленное описание")

    def test_update_lesson_by_non_owner(self):
        """Тест обновления урока не владельцем (только модератор или суперпользователь)"""
        self.client.force_authenticate(user=self.student)

        data = {"name": "Изменено студентом"}
        response = self.client.patch(
            reverse("study:lesson-update", args=[self.lesson1.id]),
            data=json.dumps(data),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Модератор может обновлять
        self.client.force_authenticate(user=self.moderator)
        response = self.client.patch(
            reverse("study:lesson-update", args=[self.lesson1.id]),
            data=json.dumps(data),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_lesson_by_owner(self):
        """Тест удаления урока владельцем"""
        self.client.force_authenticate(user=self.teacher)

        response = self.client.delete(reverse("study:lesson-delete", args=[self.lesson1.id]))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.count(), 1)

    def test_delete_lesson_by_non_owner(self):
        """Тест удаления урока не владельцем (запрещено)"""
        # Студент не может удалять
        self.client.force_authenticate(user=self.student)

        response = self.client.delete(reverse("study:lesson-delete", args=[self.lesson1.id]))

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Lesson.objects.count(), 2)

        # Модератор не может удалять (только владелец)
        self.client.force_authenticate(user=self.moderator)

        response = self.client.delete(reverse("study:lesson-delete", args=[self.lesson1.id]))

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Lesson.objects.count(), 2)

    def test_update_lesson_course_by_owner(self):
        """Тест изменения курса урока владельцем"""
        self.client.force_authenticate(user=self.teacher)

        data = {"course": self.course2.id}

        response = self.client.patch(
            reverse("study:lesson-update", args=[self.lesson1.id]),
            data=json.dumps(data),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.lesson1.refresh_from_db()
        self.assertEqual(self.lesson1.course, self.course2)


class SubscriptionTestCase(APITestCase):
    """Тестирование функционала подписок на курсы"""

    def setUp(self):
        """Настройка тестовых данных"""
        # Создание владельца курса и уроков
        self.teacher = User.objects.create(email="teacher@test.com")
        self.teacher.set_password("123")
        self.teacher.save()

        # Создание студента - подписчика курса или уроков
        self.student = User.objects.create(email="student@test.com")
        self.student.set_password("123")
        self.student.save()

        # Создание курсов
        # Создание курса учителем
        self.course1 = Course.objects.create(
            name="Python для начинающих", description="Базовый курс Python", owner=self.teacher
        )

        self.course2 = Course.objects.create(
            name="Django разработка", description="Курс по Django фреймворку", owner=self.teacher
        )

        # Создание уроков учителем
        self.lesson1 = Lesson.objects.create(
            name="Введение в Python",
            description="Основы языка Python",
            course=self.course1,
            owner=self.teacher,
            url="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        )

        self.lesson2 = Lesson.objects.create(
            name="Установка Django",
            description="Как установить Django",
            course=self.course1,
            owner=self.teacher,
            url="https://www.youtube.com/watch?v=test123",
        )

    def test_create_subscription(self):
        """Тест создания подписки на курс"""
        # Проверяем, что подписок нет
        self.client.force_authenticate(user=self.student)
        self.assertEqual(Subscription.objects.count(), 0)

        # Создаем подписку
        subscription = Subscription.objects.create(course=self.course1, user=self.student, is_active=True)

        self.assertEqual(Subscription.objects.count(), 1)
        self.assertTrue(subscription.is_active)
        self.assertEqual(subscription.user, self.student)
        self.assertEqual(subscription.course, self.course1)

    def test_toggle_subscription(self):
        """Тест включения/выключения подписки"""
        # Создаем подписку
        subscription = Subscription.objects.create(course=self.course1, user=self.student, is_active=True)

        # Выключаем подписку
        subscription.is_active = False
        subscription.save()

        subscription.refresh_from_db()
        self.assertFalse(subscription.is_active)

        # Включаем обратно
        subscription.is_active = True
        subscription.save()

        subscription.refresh_from_db()
        self.assertTrue(subscription.is_active)

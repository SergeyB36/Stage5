from django.db import models

from config import settings


class Course(models.Model):
    name = models.CharField(max_length=300, verbose_name="Название курса", help_text="Название курса")
    avatar = models.ImageField(upload_to="course/image", blank=True, null=True, verbose_name="Превью")
    description = models.TextField(blank=False, verbose_name="Описание")

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name="Владелец ресурса", on_delete=models.CASCADE, null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата последнего обновления")

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"

    def __str__(self):
        return f"Курс '{self.name}'"


class Lesson(models.Model):
    name = models.CharField(max_length=300, verbose_name="Название урока", help_text="Название курса")
    description = models.TextField(blank=False, verbose_name="Описание")
    avatar = models.ImageField(upload_to="course/image", blank=True, null=True, verbose_name="Превью")
    url = models.URLField(
        blank=True,
        null=True,
    )
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="lessons", verbose_name="Курс")
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name="Владелец ресурса", on_delete=models.CASCADE, null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата последнего обновления")

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"

    def __str__(self):
        return f"Урок '{self.name}'"

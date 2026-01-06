from django.db import models


class Course(models.Model):
    name = models.CharField(max_length=300, verbose_name="Название курса", help_text="Название курса")
    avatar = models.ImageField(upload_to="course/image", blank=True, null=True, verbose_name="Превью")
    description = models.TextField(blank=False, verbose_name="Описание")

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"

    def __str__(self):
        return f"{self.name}"


class Lesson(models.Model):
    name = models.CharField(max_length=300, verbose_name="Название урока", help_text="Название курса")
    description = models.TextField(blank=False, verbose_name="Описание")
    avatar = models.ImageField(upload_to="course/image", blank=True, null=True, verbose_name="Превью")
    url = models.URLField(blank=True, null=True,)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="lessons", verbose_name="Курс")

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"

        def __str__(self):
            return f"{self.name}"

from django.db import models


class Course(models.Model):
    name = models.CharField(max_length=300, verbose_name="Название курса", help_text="Название курса")
    avatar = models.ImageField(upload_to="course/image", blank=True, null=True, verbose_name="Превью")
    description = models.TextField(blank=False, verbose_name="Описание")

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"

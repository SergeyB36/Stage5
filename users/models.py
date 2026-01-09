from django.contrib.auth.models import AbstractUser
from django.db import models

from config import settings
from study.models import Course, Lesson


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name="Адрес электронной почты")
    avatar = models.ImageField(upload_to="users/image", blank=True, null=True, verbose_name="Аватар")
    phone_number = models.CharField(max_length=15, blank=True, null=True, verbose_name="Номер телефона")
    country = models.CharField(max_length=50, blank=True, null=True, verbose_name="Страна проживания")
    token = models.CharField(max_length=100, blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email


class Payments(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="user", verbose_name="Пользователь")
    payment_date = models.DateField(verbose_name="Дата оплаты", auto_now_add=True)
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, blank=True, null=True, related_name="paid_object", verbose_name="Курс"
    )
    lesson = models.ForeignKey(
        Lesson, on_delete=models.CASCADE, blank=True, null=True, related_name="paid_object", verbose_name="Урок"
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Сумма оплаты")
    TYPE_PAYMENT_CHOICES = [
        ("cash", "Наличные"),
        ("on_line", "Перевод на счет"),
    ]
    type_payment = models.CharField(
        max_length=20, choices=TYPE_PAYMENT_CHOICES, default=None, verbose_name="Способ оплаты"
    )

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"
        ordering = ("-payment_date",)

    def __str__(self):
        if self.course:
            return f"{self.user} - {self.course.name} - {self.amount}"
        elif self.lesson:
            return f"{self.user} - {self.lesson.name} - {self.amount}"
        return f"{self.user} - {self.amount}"

    def clean(self):
        """Валидация модели"""
        from django.core.exceptions import ValidationError

        # Проверяем, что выбран только один объект
        if self.course and self.lesson:
            raise ValidationError("Выберите только один объект: курс ИЛИ урок")

        if not self.course and not self.lesson:
            raise ValidationError("Выберите объект для оплаты: курс ИЛИ урок")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class Subscription(models.Model):
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="subscription_course", verbose_name="Подписка"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="Пользователь",
        related_name="user_subscription",
        on_delete=models.CASCADE,
    )
    is_active = models.BooleanField(default=True, blank=True, null=True)

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"
        unique_together = ["user", "course"]

    def __str__(self):
        return f"Подписка на курс {self.course}"

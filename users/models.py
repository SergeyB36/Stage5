from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone

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
    OBJECT_TYPE_CHOICES = [
        ("course", "Курс"),
        ("lesson", "Урок"),
    ]
    object_payment = models.CharField(max_length=10, choices=OBJECT_TYPE_CHOICES, verbose_name="Тип объекта оплаты")
    amount = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Сумма оплаты", validators=[MinValueValidator(0.01)]
    )
    TYPE_PAYMENT_METHOD = [
        ("cash", "Наличные"),
        ("on_line", "Перевод на счет"),
    ]
    payment_method = models.CharField(
        max_length=20, choices=TYPE_PAYMENT_METHOD, default=None, verbose_name="Способ оплаты"
    )

    session_id = models.CharField(
        max_length=255, blank=True, null=True, verbose_name="ID сессии", help_text="Укажите ID сессии"
    )

    pyment_link = models.URLField(
        max_length=600, blank=True, null=True, verbose_name="Ссылка на оплату", help_text="Укажите ссылку на оплату"
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

        if self.object_payment == "course" and not self.course:
            raise ValidationError("Для типа 'курс' необходимо выбрать курс")

        if self.object_payment == "lesson" and not self.lesson:
            raise ValidationError("Для типа 'урок' необходимо выбрать урок")

        if self.course and self.lesson:
            raise ValidationError("Выберите только один объект: курс ИЛИ урок")

        if self.object_payment == "course" and self.lesson:
            raise ValidationError("Тип 'курс', но выбран урок")

        if self.object_payment == "lesson" and self.course:
            raise ValidationError("Тип 'урок', но выбран курс")

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
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.TimeField(auto_now=True, verbose_name="Дата последнего обновления")

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"
        unique_together = ["user", "course"]

    def __str__(self):
        return f"Подписка на курс {self.course}"

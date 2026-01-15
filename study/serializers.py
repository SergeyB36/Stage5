from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from study.models import Course, Lesson
from study.servicies import get_email_subscribes
from study.tasks import send_info_about_update
from study.validators import URLValidator
from users.models import Subscription


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = ("id", "name", "description", "course", "url", "updated_at", "owner")
        validators = [URLValidator(field="url")]

    def create(self, validated_data):
        from django.utils import timezone

        lesson = Lesson.objects.create(**validated_data)

        if lesson.course:
            lesson.course.updated_at = timezone.now()
            lesson.course.save(update_fields=["updated_at"])

            # Отправка сообщения об обновлении курса
            email = get_email_subscribes(lesson.course)
            send_info_about_update.delay(email, lesson.course.id)

        return lesson


class LessonUpdateSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = ["name", "description", "avatar", "url", "course", "updated_at"]
        read_only_fields = ["owner", "created_at"]

    def update(self, obj, validated_data):
        """Обновление даты изменения"""
        from django.utils import timezone

        for attr, value in validated_data.items():
            setattr(obj, attr, value)

        obj.updated_at = timezone.now()
        obj.save()
        course = Course.objects.get(id=obj.course_id)
        course.updated_at = timezone.now()
        course.save()

        # Отправка сообщения об обновлении курса
        email = get_email_subscribes(course)
        send_info_about_update.delay(email, course.id)
        return obj


class CourseSerializer(ModelSerializer):
    subscribes_count = SerializerMethodField()
    course_lesson_count = SerializerMethodField()
    is_subscribe = SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = (
            "id",
            "name",
            "description",
            "owner",
            "course_lesson_count",
            "lessons",
            "is_subscribe",
            "updated_at",
            "subscribes_count",
        )

    read_only_fields = ["id", "owner", "created_at"]

    def get_course_lesson_count(self, obj):
        """Количество уроков в курсе"""
        return obj.lessons.count()

    def get_is_subscribe(self, obj):
        """Функция подписки на курс"""
        request = self.context.get("request")
        if not request or not request.user.is_authenticated:
            return False
        return Subscription.objects.filter(user=request.user, course=obj, is_active=True).exists()

    def get_subscribes_count(self, obj):
        """Получаем количество подписок"""
        return obj.subscription_course.count()

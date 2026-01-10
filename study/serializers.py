from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from study.models import Course, Lesson
from study.validators import URLValidator
from users.models import Subscription


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = ("id", "name", "description", "course", "url")
        validators = [URLValidator(field="url")]


class CourseSerializer(ModelSerializer):
    course_lesson_count = SerializerMethodField()
    is_subscribe = SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ("id", "name", "description", "course_lesson_count", "lessons", "is_subscribe")

    def get_course_lesson_count(self, obj):
        return obj.lessons.count()

    def get_is_subscribe(self, obj):
        request = self.context.get("request")
        if not request or not request.user.is_authenticated:
            return False
        return Subscription.objects.filter(user=request.user, course=obj, is_active=True).exists()

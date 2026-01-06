from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from study.models import Course, Lesson


class CourseSerializer(ModelSerializer):
    course_lesson_count = SerializerMethodField()

    class Meta:
        model = Course
        fields = ("id", "name", "description", "course_lesson_count")

    def get_course_lesson_count(self, obj):
        return obj.lessons.all().count()


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = ("id", "name", "description", "course")
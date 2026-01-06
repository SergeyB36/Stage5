from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from study.models import Course, Lesson


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = ("id", "name", "description", "course")


class CourseSerializer(ModelSerializer):
    course_lesson_count = SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ("id", "name", "description", "course_lesson_count", "lessons")

    def get_course_lesson_count(self, obj):
        return obj.lessons.count()

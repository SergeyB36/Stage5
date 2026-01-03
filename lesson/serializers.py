from rest_framework.serializers import ModelSerializer

from lesson.models import Lesson


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"

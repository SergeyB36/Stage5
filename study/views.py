from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from study.models import Course, Lesson
from study.permissions import IsOwnerOrIsModerator, IsOwner, CanCreatePermission
from study.serializers import CourseSerializer, LessonSerializer


class LessonCreateAPIView(CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [CanCreatePermission]


    def perform_create(self, serializer):
        lesson = serializer.save(owner=self.request.user)


class LessonListAPIView(ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonRetrieveAPIView(RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonUpdateAPIView(UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsOwnerOrIsModerator]


class LessonDestroyAPIView(DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsOwner]


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [AllowAny]
        if self.action == 'create':
            permission_classes = [CanCreatePermission]
        if self.action == 'retrieve':
            permission_classes = [AllowAny]
        if self.action == 'update':
            permission_classes = [IsOwnerOrIsModerator]
        if self.action == 'partial_update':
            permission_classes = [IsOwnerOrIsModerator]
        if self.action == 'destroy':
            permission_classes = [IsOwner]
        return [permission() for permission in permission_classes]

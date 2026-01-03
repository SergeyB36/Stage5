from django.conf.urls.static import static
from django.urls import path
from rest_framework.routers import SimpleRouter

from config import settings
from course.views import CourseViewSet
from lesson.apps import LessonConfig
from lesson.views import (
    LessonCreateAPIView,
    LessonDestroyAPIView,
    LessonListAPIView,
    LessonRetrieveAPIView,
    LessonUpdateAPIView,
)

app_name = LessonConfig.name

router = SimpleRouter()
router.register("", CourseViewSet)

urlpatterns = [
    path("lesson/create/", LessonCreateAPIView.as_view(), name="lesson_create"),
    path("lesson/", LessonListAPIView.as_view(), name="lesson_list"),
    path("lesson/<int:pk>/", LessonRetrieveAPIView.as_view(), name="lesson_retrieve"),
    path("lesson/<int:pk>/delete/", LessonDestroyAPIView.as_view(), name="lesson_delete"),
    path("lesson/<int:pk>/update/", LessonUpdateAPIView.as_view(), name="lesson_update"),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

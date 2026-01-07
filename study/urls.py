from django.conf.urls.static import static
from django.urls import path
from rest_framework.routers import SimpleRouter

from config import settings
from study.apps import StudyConfig
from study.views import (
    CourseViewSet,
    LessonCreateAPIView,
    LessonDestroyAPIView,
    LessonListAPIView,
    LessonRetrieveAPIView,
    LessonUpdateAPIView,
)

app_name = StudyConfig.name

router = SimpleRouter()
router.register("", CourseViewSet)

urlpatterns = [
    path("lesson/create/", LessonCreateAPIView.as_view(), name="lesson-create"),
    path("lesson/", LessonListAPIView.as_view(), name="lesson-list"),
    path("lesson/<int:pk>/", LessonRetrieveAPIView.as_view(), name="lesson-retrieve"),
    path("lesson/<int:pk>/delete/", LessonDestroyAPIView.as_view(), name="lesson-delete"),
    path("lesson/<int:pk>/update/", LessonUpdateAPIView.as_view(), name="lesson-update"),
]

urlpatterns += router.urls

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

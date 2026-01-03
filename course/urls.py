from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import SimpleRouter

from course.apps import CourseConfig
from course.views import CourseViewSet

app_name = CourseConfig.name

router = SimpleRouter()
router.register("", CourseViewSet)

urlpatterns = []

urlpatterns += router.urls

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

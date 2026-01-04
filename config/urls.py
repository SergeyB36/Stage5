from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("course/", include("course.urls", namespace="course")),
    path("lesson/", include("lesson.urls", namespace="lesson")),
    path("study/", include("study.urls", namespace="study")),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

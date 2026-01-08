from django.conf.urls.static import static
from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from config import settings
from users.apps import UsersConfig
from users.views import (
    CustomUserCreateAPIView,
    PaymentsCreateAPIView,
    PaymentsListAPIView,
    PaymentsRetrieveAPIView,
)

app_name = UsersConfig.name


urlpatterns = [
    path("payments/create/", PaymentsCreateAPIView.as_view(), name="payment-create"),
    path("payments/", PaymentsListAPIView.as_view(), name="payment-list"),
    path("payments/<int:pk>/", PaymentsRetrieveAPIView.as_view(), name="payment-retrieve"),
    path("login/", TokenObtainPairView.as_view(permission_classes=(AllowAny,)), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(permission_classes=(AllowAny,)), name="token_refresh"),
    path("register/", CustomUserCreateAPIView.as_view(), name="register"),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

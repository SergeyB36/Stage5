from django.conf.urls.static import static
from django.urls import path

from config import settings

from users.apps import UsersConfig
from users.views import PaymentsCreateAPIView, PaymentsRetrieveAPIView, PaymentsListAPIView

app_name = UsersConfig.name


urlpatterns = [
    path("payments/create/", PaymentsCreateAPIView.as_view(), name="payment-create"),
    path("payments/", PaymentsListAPIView.as_view(), name="payment-list"),
    path("payments/<int:pk>/", PaymentsRetrieveAPIView.as_view(), name="payment-retrieve"),
    # path("payments/<int:pk>/delete/", PaymentsDestroyAPIView.as_view(), name="payments-delete"),
    # path("payments/<int:pk>/update/", PaymentsUpdateAPIView.as_view(), name="payments-update"),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView

from users.models import Payments
from users.serializers import PaymentsSerializer


class PaymentsCreateAPIView(CreateAPIView):
    queryset = Payments.objects.all()
    serializer_class = PaymentsSerializer


class PaymentsListAPIView(ListAPIView):
    queryset = Payments.objects.all()
    serializer_class = PaymentsSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["payment_date", "course", "lesson", "type_payment"]


class PaymentsRetrieveAPIView(RetrieveAPIView):
    queryset = Payments.objects.all()
    serializer_class = PaymentsSerializer

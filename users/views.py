from rest_framework.generics import CreateAPIView

from users.models import Payments
from users.serializers import PaymentsSerializer


class PaymentsCreateAPIView(CreateAPIView):
    queryset = Payments.objects.all()
    serializer_class = PaymentsSerializer
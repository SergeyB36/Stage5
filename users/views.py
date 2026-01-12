from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from requests import session
from rest_framework import status
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveAPIView,
)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from study.models import Course
from study.permissions import CanCreatePermission
from users.models import CustomUser, Payments, Subscription
from users.serializers import (
    CustomUserSerializer,
    PaymentsSerializer,
    SubscriptionSerializer, PaymentsCreateSerializer,
)
from users.servicies import create_price, create_session


class PaymentsCreateAPIView(CreateAPIView):
    queryset = Payments.objects.all()
    serializer_class = PaymentsCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        payment = serializer.save(user=self.request.user)
        amount = create_price(payment.amount)
        session_id, pyment_link = create_session(amount)
        payment.session_id = session_id
        payment.pyment_link = pyment_link
        payment.save()



class PaymentsListAPIView(ListAPIView):
    queryset = Payments.objects.all()
    serializer_class = PaymentsSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["payment_date", "course", "lesson", "type_payment"]


class PaymentsRetrieveAPIView(RetrieveAPIView):
    queryset = Payments.objects.all()
    serializer_class = PaymentsSerializer


class CustomUserCreateAPIView(CreateAPIView):
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class SubscriptionCreateAPIView(CreateAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = [CanCreatePermission]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def post(self, *args, **kwargs):
        user = self.request.user
        course_id = self.request.data.get("course_id")
        course = get_object_or_404(Course, id=course_id)

        subscription = Subscription.objects.filter(user=user, course=course).first()
        sub_q = Subscription.objects.filter(user=user, course=course)
        if sub_q.exists() and subscription.is_active:
            subscription.is_active = False
            subscription.save()
            message = "Подписка удалена"
            http_status = status.HTTP_200_OK
        elif sub_q.exists() and not subscription.is_active:
            subscription.is_active = True
            subscription.save()
            message = "Подписка добавлена"
            http_status = status.HTTP_200_OK
        else:
            subscription = Subscription.objects.create(user=user, course=course)
            subscription.is_active = True
            subscription.save()
            message = "подписка добавлена"
            http_status = status.HTTP_201_CREATED
        return Response(
            {"message": message},
            status=http_status,
        )

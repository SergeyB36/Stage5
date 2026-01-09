from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from users.models import CustomUser, Payments, Subscription


class CustomUserSerializer(ModelSerializer):
    subscriptions = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = "__all__"

    def get_subscriptions(self, obj):
        return [sub for sub in obj.user_subscription.all() if sub.is_active is True]


class PaymentsSerializer(ModelSerializer):

    class Meta:
        model = Payments
        fields = "__all__"


class PaymentsCreateSerializer(ModelSerializer):
    class Meta:
        model = Payments
        fields = (
            "user",
            "payment_amount",
            "course",
            "lesson",
            "payment_method",
        )

    def create(self, validated_data):
        from django.utils import timezone

        validated_data["payment_date"] = timezone.now()

        course = validated_data.get("course")
        lesson = validated_data.get("lesson")

        if course:
            validated_data["type_payment"] = "course"
        elif lesson:
            validated_data["type_payment"] = "lesson"

        return super().create(validated_data)


class SubscriptionSerializer(ModelSerializer):
    course_name = serializers.CharField(source="course.name", read_only=True)
    user_email = serializers.CharField(source="user.email", read_only=True)

    class Meta:
        model = Subscription
        fields = (
            "id",
            "user_email",
            "course_name",
            "is_active",
        )

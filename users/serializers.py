from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from users.models import CustomUser, Payments, Subscription


class CustomUserSerializer(ModelSerializer):
    subscriptions = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ("id", "email", "avatar", "phone_number", "country", "subscriptions")

    def get_subscriptions(self, obj):
        return obj.user_subscription.filter(is_active=True)


class PaymentsSerializer(ModelSerializer):

    class Meta:
        model = Payments
        fields = "__all__"


class PaymentsCreateSerializer(ModelSerializer):
    class Meta:
        model = Payments
        fields = (
            "user",
            "amount",
            "course",
            "lesson",
            "payment_method",
            "object_payment",
        )

    def create(self, validated_data):
        from django.utils import timezone

        validated_data["payment_date"] = timezone.now()

        course = validated_data.get("course")
        lesson = validated_data.get("lesson")

        if course:
            validated_data["object_payment"] = "course"
        elif lesson:
            validated_data["object_payment"] = "lesson"

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

from rest_framework.serializers import ModelSerializer

from users.models import Payments


class PaymentsSerializer(ModelSerializer):

    class Meta:
        model = Payments
        fields = "__all__"


class PaymentsCreateSerializer(ModelSerializer):
    # Только необходимые поля для создания
    class Meta:
        model = Payments
        fields = (
            "user",
            "payment_amount",
            "type_payment",
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

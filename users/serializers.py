from rest_framework.fields import SerializerMethodField
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
        # Можно добавить дополнительную логику при создании
        # Например, автоматически установить дату оплаты
        from django.utils import timezone
        validated_data['payment_date'] = timezone.now()

        # Проверяем, что выбран либо курс, либо урок
        course = validated_data.get('course')
        lesson = validated_data.get('lesson')

        if course:
            validated_data['type_payment'] = 'course'
        elif lesson:
            validated_data['type_payment'] = 'lesson'

        return super().create(validated_data)

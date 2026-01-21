from rest_framework import serializers
from .models import PaymentEvent
from .services.parser import normalize_event_type

class PaymentEventListSerializer(serializers.ModelSerializer):
    event_type = serializers.SerializerMethodField()

    class Meta:
        model = PaymentEvent
        fields = ["event_type", "received_at"]

    def get_event_type(self, obj: PaymentEvent) -> str:
        return normalize_event_type(obj.event_type)
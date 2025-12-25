from django.utils import timezone
from rest_framework import serializers
from django.core.exceptions import ValidationError
from rentals.models import Booking

class BookingSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    status = serializers.CharField(read_only=True)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Booking
        fields = ("id", "listing", "user", "start_date", "end_date", "status", "total_price", "created_at")
        read_only_fields = ("status", "total_price", "created_at")

    def validate(self, data):
        start = data.get("start_date")
        end = data.get("end_date")
        if start is None or end is None:
            raise serializers.ValidationError("Start- und Enddatum erforderlich.")
        if start >= end:
            raise serializers.ValidationError("Start muss vor Ende liegen.")
        if end <= timezone.now().date():
            raise serializers.ValidationError("Enddatum muss in der Zukunft liegen.")
        return data

    def create(self, validated_data):
        request = self.context.get("request")
        if not request or not request.user.is_authenticated:
            raise serializers.ValidationError("Authentifizierung erforderlich.")
        validated_data["user"] = request.user
        booking = Booking(**validated_data)
        try:
            booking.full_clean()  # ruft model.clean(), inkl. Überlappungsprüfung
        except ValidationError as e:
            raise serializers.ValidationError(e.message_dict if hasattr(e, "message_dict") else e.messages)
        booking.save()
        return booking
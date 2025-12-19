from rest_framework import serializers
from rentals.models import Review

class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = ("id", "listing", "user", "rating", "comment", "created_at")
        read_only_fields = ("created_at",)

    def validate_rating(self, value):
        if not (1 <= value <= 5):
            raise serializers.ValidationError("Rating muss zwischen 1 und 5 liegen.")
        return value

    def create(self, validated_data):
        request = self.context.get("request")
        if not request or not request.user.is_authenticated:
            raise serializers.ValidationError("Authentifizierung erforderlich.")
        validated_data["user"] = request.user
        # unique_together modelseitig verhindert Doppelbewertungen; fangen wir freundlich ab
        if Review.objects.filter(listing=validated_data["listing"], user=validated_data["user"]).exists():
            raise serializers.ValidationError("Du hast dieses Angebot bereits bewertet.")
        return super().create(validated_data)
from rest_framework import serializers
from rentals.models import SearchQuery

class SearchQuerySerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = SearchQuery
        fields = ("id", "user", "query", "created_at", "count")
        read_only_fields = ("created_at", "count")

    def create(self, validated_data):
        request = self.context.get("request")
        user = request.user if request and request.user.is_authenticated else None
        q = validated_data.get("query", "").strip()
        if not q:
            raise serializers.ValidationError("Leere Suchanfrage.")
        obj, created = SearchQuery.objects.get_or_create(query=q, user=user)
        if not created:
            obj.count = obj.count + 1
            obj.save(update_fields=["count"])
        return obj
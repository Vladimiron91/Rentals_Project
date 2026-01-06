from rest_framework import serializers
from rentals.models import ListingView

class ListingViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListingView
        fields = ("id", "user", "listing", "viewed_at", "ip_address")
        read_only_fields = ("viewed_at", "ip_address")
from rest_framework import serializers
from rentals.models import ListingImage

class ListingImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField()

    class Meta:
        model = ListingImage
        fields = ("id", "listing", "image", "alt_text")
        read_only_fields = ("id",)
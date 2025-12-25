from rest_framework import serializers
from django.db.models import Count
from rentals.models import Listing

class ListingCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Listing
        fields = ("id", "title", "description", "location", "price", "rooms", "property_type", "is_active")

class ListingSerializer(serializers.ModelSerializer):
    owner = serializers.SerializerMethodField(read_only=True)
    images = serializers.SerializerMethodField(read_only=True)
    reviews_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Listing
        fields = ("id", "owner", "title", "description", "location", "price", "rooms",
                  "property_type", "is_active", "created_at", "views_count", "images", "reviews_count")

    def get_owner(self, obj):
        return {"id": obj.owner.id, "username": obj.owner.username}

    def get_images(self, obj):
        # vermeide heavy nested serializers hier; nur URL + alt_text
        return [{"id": i.id, "image": getattr(i.image, "url", None), "alt_text": i.alt_text} for i in obj.images.all()]

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        # falls queryset in View mit .annotate(reviews_count=Count('reviews')) vorannotiert ist, bleibt field gefüllt
        if "reviews_count" not in rep or rep["reviews_count"] is None:
            rep["reviews_count"] = getattr(instance, "reviews_count", instance.reviews.count())
        return rep

from rest_framework import generics, permissions, filters
from rest_framework.exceptions import PermissionDenied
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count

from rentals.models import Listing
from rentals.serializers import (
    ListingSerializer,
    ListingCreateUpdateSerializer
)


class ListingListCreateView(generics.ListCreateAPIView):
    queryset = Listing.objects.all().annotate(
        reviews_count=Count("reviews")
    )
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    filterset_fields = ["property_type", "rooms", "price", "location", "is_active"]
    search_fields = ["title", "description", "location"]
    ordering_fields = ["price", "created_at", "views_count"]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return ListingCreateUpdateSerializer
        return ListingSerializer

    def perform_create(self, serializer):
        profile = getattr(self.request.user, "profile", None)
        if not profile or profile.role != "landlord":
            raise PermissionDenied("Nur Vermieter können Anzeigen erstellen.")
        serializer.save(owner=self.request.user)


class ListingDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Listing.objects.all().annotate(
        reviews_count=Count("reviews")
    )
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.request.method in ["PUT", "PATCH"]:
            return ListingCreateUpdateSerializer
        return ListingSerializer

    def perform_update(self, serializer):
        if serializer.instance.owner != self.request.user:
            raise PermissionDenied("Nur der Eigentümer darf ändern.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.owner != self.request.user:
            raise PermissionDenied("Nur der Eigentümer darf löschen.")
        instance.delete()
from rest_framework import viewsets, permissions
from rest_framework.exceptions import PermissionDenied

from rentals.models import ListingImage, Listing
from rentals.serializers import ListingImageSerializer


class ListingImageViewSet(viewsets.ModelViewSet):
    queryset = ListingImage.objects.all()
    serializer_class = ListingImageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        listing = Listing.objects.get(pk=self.request.data.get("listing"))
        if listing.owner != self.request.user:
            raise PermissionDenied("Nur der Eigentümer darf Bilder hochladen.")
        serializer.save()
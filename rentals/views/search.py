from rest_framework import generics, permissions
from rentals.models import SearchQuery
from rentals.serializers import SearchQuerySerializer


class SearchQueryView(generics.ListCreateAPIView):
    queryset = SearchQuery.objects.all().order_by("-count", "-created_at")
    serializer_class = SearchQuerySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
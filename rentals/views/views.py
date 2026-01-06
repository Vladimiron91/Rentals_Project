from django.db import transaction
from django.db import models
from django.utils import timezone
from rest_framework import generics, permissions
from rest_framework.response import Response
from rentals.models import Listing, ListingView
from rentals.serializers import ListingViewSerializer


class ListingViewCreateView(generics.CreateAPIView):
    """
    Сохраняет просмотр объявления и увеличивает счетчик views_count.
    Вызывается при каждом открытии страницы объявления.
    """
    serializer_class = ListingViewSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        listing_id = request.data.get("listing")
        if not listing_id:
            return Response({"error": "listing ID required"}, status=400)

        try:
            listing = Listing.objects.get(id=listing_id)
        except Listing.DoesNotExist:
            return Response({"error": "Listing not found"}, status=404)

        user = request.user if request.user.is_authenticated else None

        with transaction.atomic():
            # Увеличиваем счетчик просмотров (используем F() для атомарности)
            listing.views_count = models.F('views_count') + 1
            listing.save(update_fields=['views_count'])

            # Обновляем listing из базы, чтобы получить актуальное значение views_count
            listing.refresh_from_db()

            # Сохраняем историю просмотра
            view, created = ListingView.objects.get_or_create(
                user=user,
                listing=listing,
                defaults={'ip_address': self.get_client_ip(request)}
            )

        return Response({
            "message": "View recorded",
            "views_count": listing.views_count,
            "view_id": view.id
        }, status=201)

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
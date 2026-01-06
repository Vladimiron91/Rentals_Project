from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rentals.models import Booking
from rentals.serializers import BookingSerializer


class BookingConfirmView(generics.UpdateAPIView):
    """
    Арендодатель подтверждает бронирование.
    """
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        booking = self.get_object()

        # Проверяем, что пользователь - владелец объявления
        if booking.listing.owner != request.user:
            raise PermissionDenied("Только владелец объявления может подтверждать бронирования.")

        # Проверяем, что бронирование в статусе pending
        if booking.status != Booking.STATUS_PENDING:
            return Response(
                {"error": f"Бронирование уже в статусе {booking.status}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        booking.status = Booking.STATUS_CONFIRMED
        booking.save(update_fields=['status'])

        return Response({
            "message": "Бронирование подтверждено",
            "booking_id": booking.id,
            "status": booking.status
        })


class BookingDeclineView(generics.UpdateAPIView):
    """
    Арендодатель отклоняет бронирование.
    """
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        booking = self.get_object()

        # Проверяем, что пользователь - владелец объявления
        if booking.listing.owner != request.user:
            raise PermissionDenied("Только владелец объявления может отклонять бронирования.")

        # Проверяем, что бронирование в статусе pending
        if booking.status != Booking.STATUS_PENDING:
            return Response(
                {"error": f"Бронирование уже в статусе {booking.status}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        booking.status = Booking.STATUS_DECLINED
        booking.save(update_fields=['status'])

        return Response({
            "message": "Бронирование отклонено",
            "booking_id": booking.id,
            "status": booking.status
        })
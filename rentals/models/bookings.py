from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
# Verwende String-Referenz für Listing, da das Modell in einer anderen Datei definiert ist: "rentals.Listing"

class Booking(models.Model):
    '''Buchung eines Listings für einen Zeitraum.'''
    STATUS_PENDING = "pending"
    STATUS_CONFIRMED = "confirmed"
    STATUS_DECLINED = "declined"
    STATUS_CANCELLED = "cancelled"
    STATUS_REJECTED = "rejected"
    STATUS_COMPLETED = "completed"
    STATUS_CHOICES = (
        (STATUS_PENDING, "Ausstehend"),
        (STATUS_CONFIRMED, "Bestätigt"),
        (STATUS_DECLINED, "Storniert"),
        (STATUS_CANCELLED, "Abgelehnt"),
        (STATUS_REJECTED, "rejected"),
        (STATUS_COMPLETED, "completed"),
    )

    # Beziehungen
    # Eine Buchung gehört zu einer Anzeige
    listing = models.ForeignKey("rentals.Listing", on_delete=models.CASCADE, related_name="bookings")
    # Benutzer, der die Buchung erstellt hat (Mieter)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="bookings")
    # Buchungszeitraum
    start_date = models.DateField()  # Start
    end_date = models.DateField()  # Ende

    # Erstellungsdatum
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]

    def clean(self):
        """
        Validierung: start < end und keine Überlappung mit bestätigten Buchungen.
        """
        if self.start_date >= self.end_date:
            raise ValidationError("Дата начала должна быть раньше даты окончания.")
        overlapping = Booking.objects.filter(
            listing=self.listing,
            status=self.STATUS_CONFIRMED,
            start_date__lt=self.end_date,
            end_date__gt=self.start_date,
        ).exclude(pk=self.pk)
        if overlapping.exists():
            raise ValidationError("Это место уже занято в выбранные даты.")

    def save(self, *args, **kwargs):
        # Berechne total_price als price * nights (sofern Listing vorhanden)
        try:
            nights = (self.end_date - self.start_date).days
        except Exception:
            nights = 0
        if nights > 0:
            # Lazy lookup der Listing-Instanz (ForeignKey-Objekt kann bereits geladen sein)
            if hasattr(self, "listing") and self.listing is not None:
                try:
                    self.total_price = self.listing.price * nights
                except Exception:
                    pass
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Booking {self.pk} by {self.user} ({self.start_date} — {self.end_date})"
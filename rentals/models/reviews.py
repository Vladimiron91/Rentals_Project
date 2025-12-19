from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator

class Review(models.Model):
    """
    Bewertung/Kommentar für ein Listing. Ein User darf nur einen Review pro Listing schreiben.
    """
    # Wenn die Anzeige gelöscht wird, werden alle Bewertungen ebenfalls gelöscht
    listing = models.ForeignKey("rentals.Listing", on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reviews")
    # Bewertung (0–5 Sterne)
    rating = models.FloatField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(5)
        ]
    )
    # Kommentar des Mieters
    comment = models.TextField(blank=True)
    # Erstellungsdatum der Bewertung
    created_at = models.DateTimeField(auto_now_add=True)

    # Beschränkung (wie bei Airbnb, 1 Nutzer – 1 Bewertung)
    class Meta:
        ordering = ["-created_at"]
        unique_together = ("listing", "user")

    def __str__(self):
        return f"Bewertung {self.rating} von {self.user} für {self.listing}"

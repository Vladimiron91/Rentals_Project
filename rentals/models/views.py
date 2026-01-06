from django.db import models
from django.conf import settings


class ListingView(models.Model):
    """
    История просмотров объявлений.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="viewed_listings"
    )
    listing = models.ForeignKey(
        "rentals.Listing",
        on_delete=models.CASCADE,
        related_name="views_history"
    )
    viewed_at = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    class Meta:
        ordering = ["-viewed_at"]
        unique_together = ["user", "listing"]

    def __str__(self):
        return f"{self.user or 'Anonymous'} viewed {self.listing} at {self.viewed_at}"
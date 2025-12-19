from django.db import models
from django.conf import settings

class SearchQuery(models.Model):
    """
    Gespeicherte Suchbegriffe inkl. Zähler für Popularität.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    query = models.CharField(max_length=255, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    count = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ["-count", "-created_at"]

    def __str__(self):
        return f"{self.query} ({self.count})"
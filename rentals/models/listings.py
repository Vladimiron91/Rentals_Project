from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator

#Wohnungstypen
class PropertyType(models.TextChoices):
    APARTMENT = "apartment", "Wohnung"
    HOUSE = "house", "Haus"
    STUDIO = "studio", "Studio"
    room = "room", "Zimmer"

#Imobilienanzeigen

class Listing(models.Model):
    '''Hauptmodell für ein Immobilien-Angebot'''

    #Eigentümer der Anzeige(Vermieter)
    #One-to-Many: Ein Benutzer kann mehrere Anzeigen haben
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="listings")
    #Preis, Anzahl der Zimmer und Immobilientyp
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255) #Stadt / Bezirk

    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    rooms = models.PositiveIntegerField()
    property_type = models.CharField(max_length=20, choices=PropertyType.choices)

    #Aktiv / Inaktiv (Anzeige sichtbar oder verborgen)
    is_active = models.BooleanField

    #Systemfelder
    created_at = models.DateTimeField(auto_now_add=True)
    views_count = models.PositiveIntegerField(default=0)

    #Lesbare Darstellung der Anzeige
    def __str__(self):
        return f"{self.title} - {self.location}"

#Bildmaterial zur Anzeige (optional)
class ListingImage(models.Model):
    """
    Bilder eines Listings (optional).
    """
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="listings/")
    alt_text = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"Image for listing {self.listing_id}"
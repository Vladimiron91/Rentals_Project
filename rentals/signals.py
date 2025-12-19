from django.apps import AppConfig
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db import models

from rentals.models import Profile, Listing

#Автосоздание Profile
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

class RentalsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "rentals"

    def ready(self):
        import rentals.signals

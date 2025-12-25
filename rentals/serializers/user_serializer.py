from django.db import transaction
from django.contrib.auth.models import User
from rest_framework import serializers

from rentals.models import Profile

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email", "first_name", "last_name")

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    role = serializers.ChoiceField(write_only=True, choices=(("tenant", "Mieter"), ("landlord", "Vermieter")), required=False, default="tenant")

    class Meta:
        model = User
        fields = ("id", "username", "email", "password", "first_name", "last_name", "role")

    def create(self, validated_data):
        role = validated_data.pop("role", "tenant")
        password = validated_data.pop("password")
        with transaction.atomic():
            user = User(**validated_data)
            user.set_password(password)
            user.save()
            # Profil anlegen
            Profile.objects.create(user=user, role=role)
        return user
from rest_framework import serializers
from django.contrib.auth.models import User
from rentals.models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    role = serializers.ChoiceField(choices=(("tenant", "Mieter"), ("landlord", "Vermieter")), required=False)

    class Meta:
        model = Profile
        fields = ("user", "phone", "bio", "role")
        read_only_fields = ("user",)
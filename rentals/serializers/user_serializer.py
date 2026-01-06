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
    role = serializers.ChoiceField(
        write_only=True,
        choices=(("tenant", "Mieter"), ("landlord", "Vermieter")),
        required=False,
        default="tenant"
    )

    class Meta:
        model = User
        fields = ("id", "username", "email", "password", "first_name", "last_name", "role")

    def create(self, validated_data):
        role = validated_data.pop("role", "tenant")  # Извлекаем роль
        password = validated_data.pop("password")  # Извлекаем пароль

        with transaction.atomic():
            # Создаем пользователя
            user = User(**validated_data)
            user.set_password(password)
            user.save()

            # Профиль уже создан сигналом, обновляем только роль
            # Используем get_or_create для безопасности
            profile, created = Profile.objects.get_or_create(
                user=user,
                defaults={'role': role}
            )

            # Если профиль уже существовал (маловероятно), обновляем роль
            if not created:
                profile.role = role
                profile.save(update_fields=['role'])

        return user
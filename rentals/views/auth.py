from django.contrib.auth import authenticate
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token  # ПРАВИЛЬНЫЙ ИМПОРТ!


class LoginView(APIView):
    """
    Эндпоинт для входа пользователя.
    Возвращает токен для аутентификации.
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response(
                {"error": "Пожалуйста, укажите username и password"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Аутентифицируем пользователя
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                # Получаем или создаем токен
                token, created = Token.objects.get_or_create(user=user)

                # Возвращаем информацию о пользователе и токен
                return Response({
                    "message": "Вход выполнен успешно",
                    "user_id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "token": token.key,
                    "role": user.profile.role if hasattr(user, 'profile') else 'tenant'
                })
            else:
                return Response(
                    {"error": "Учетная запись отключена"},
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            return Response(
                {"error": "Неверные учетные данные"},
                status=status.HTTP_401_UNAUTHORIZED
            )


class LogoutView(APIView):
    """
    Эндпоинт для выхода пользователя (удаление токена).
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        # Удаляем токен текущего пользователя
        try:
            request.user.auth_token.delete()
        except (AttributeError, Token.DoesNotExist):
            pass

        return Response({"message": "Выход выполнен успешно"})
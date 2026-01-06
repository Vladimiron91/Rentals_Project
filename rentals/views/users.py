from rest_framework import generics, permissions
from django.contrib.auth.models import User
from rentals.serializers import UserSerializer, UserRegisterSerializer
from rest_framework.response import Response

class UserRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.AllowAny]


class UserDetailView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

class CurrentUserView(generics.RetrieveAPIView):
    """
        Получить информацию о текущем аутентифицированном пользователе.
        """
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    def retrieve(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(user)

        # Добавляем информацию о профиле
        data = serializer.data
        if hasattr(user, 'profile'):
            data['role'] = user.profile.role
            data['phone'] = user.profile.phone
            data['bio'] = user.profile.bio

        return Response(data)
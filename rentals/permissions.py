#Разрешать редактировать / удалять объявление ТОЛЬКО владельцу"""

#никто не может редактировать чужие объявления / полностью соответствует Airbnb

from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    """
    Разрешает редактировать / удалять объявление
    ТОЛЬКО владельцу (landlord)
    """

    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_authenticated
            and hasattr(request.user, "profile")
            and request.user.profile.role == "landlord"
            and obj.owner == request.user
        )

#только landlord может создавать/редактировать объявления
#tenant — только смотреть и бронировать

class IsLandlord(BasePermission):
    """
    Разрешает действия ТОЛЬКО арендодателю
    """

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and hasattr(request.user, "profile")
            and request.user.profile.role == "landlord"
        )
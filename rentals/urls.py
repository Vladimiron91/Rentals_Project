from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    # Auth
    LoginView,
    LogoutView,
    CurrentUserView,

    # Users
    UserRegisterView,
    UserDetailView,

    # Profiles
    ProfileView,

    # Listings
    ListingListCreateView,
    ListingDetailView,

    # Images
    ListingImageViewSet,

    # Reviews
    ReviewListCreateView,
    ReviewDetailView,

    # Bookings
    BookingListCreateView,
    BookingDetailView,

    # Search
    SearchQueryView,

    # Новые импорты
    ListingSearchView,
    ListingViewCreateView,
    BookingConfirmView,
    BookingDeclineView,
)

urlpatterns = [
    # Аутентификация
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('current-user/', CurrentUserView.as_view(), name='current-user'),

    # Users
    path('register/', UserRegisterView.as_view(), name='register'),
    path('me/', UserDetailView.as_view(), name='user-detail'),

    # Profiles
    path('profile/', ProfileView.as_view(), name='profile'),

    # Listings
    path('listings/', ListingListCreateView.as_view(), name='listing-list'),
    path('listings/<int:pk>/', ListingDetailView.as_view(), name='listing-detail'),

    # Images
    path('images/', ListingImageViewSet.as_view({'get': 'list', 'post': 'create'}), name='image-list'),
    path('images/<int:pk>/', ListingImageViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}),
         name='image-detail'),

    # Reviews
    path('reviews/', ReviewListCreateView.as_view(), name='review-list'),
    path('reviews/<int:pk>/', ReviewDetailView.as_view(), name='review-detail'),

    # Bookings
    path('bookings/', BookingListCreateView.as_view(), name='booking-list'),
    path('bookings/<int:pk>/', BookingDetailView.as_view(), name='booking-detail'),

    # Search
    path('search-queries/', SearchQueryView.as_view(), name='search-query'),

    #МАРШРУТЫ:
    # Поиск с сохранением запроса
    path('listings/search/', ListingSearchView.as_view(), name='listing-search'),
    # Сохранение просмотра
    path('listings/view/', ListingViewCreateView.as_view(), name='listing-view'),
    # Подтверждение/отклонение бронирования
    path('bookings/<int:pk>/confirm/', BookingConfirmView.as_view(), name='booking-confirm'),
    path('bookings/<int:pk>/decline/', BookingDeclineView.as_view(), name='booking-decline'),
]
# import factory
# from faker import Faker
# from django.contrib.auth.hashers import make_password
# from django.utils import timezone
# from django.contrib.auth import get_user_model
#
# User = get_user_model()
# faker = Faker()
#
#
# class UserFactory(factory.django.DjangoModelFactory):
#     class Meta:
#         model = User
#         django_get_or_create = ('username',)
#
#     username = factory.LazyAttribute(lambda _: faker.unique.user_name())
#     email = factory.LazyAttribute(lambda obj: f"{obj.username}@example.com")
#     first_name = factory.Faker('first_name')
#     last_name = factory.Faker('last_name')
#     is_staff = False
#     is_active = True
#     date_joined = factory.LazyFunction(timezone.now)
#     password = factory.LazyFunction(lambda: make_password("test123"))
#
#     @classmethod
#     def create_test_users(cls):
#         """Создает тестовых пользователей Vermieter и Mieter"""
#         from django.contrib.auth import get_user_model
#         User = get_user_model()
#
#         users_data = [
#             {
#                 'username': 'vermieter1',
#                 'email': 'vermieter@example.com',
#                 'first_name': 'Max',
#                 'last_name': 'Mustermann',
#                 'password': 'test123'
#             },
#             {
#                 'username': 'mieter1',
#                 'email': 'mieter@example.com',
#                 'first_name': 'Anna',
#                 'last_name': 'Schmidt',
#                 'password': 'test123'
#             }
#         ]
#
#         created_users = []
#         for user_data in users_data:
#             user, created = User.objects.get_or_create(
#                 username=user_data['username'],
#                 defaults={
#                     'email': user_data['email'],
#                     'first_name': user_data['first_name'],
#                     'last_name': user_data['last_name']
#                 }
#             )
#             if created or not user.check_password(user_data['password']):
#                 user.set_password(user_data['password'])
#                 user.save()
#
#             created_users.append(user)
#
#         return created_users

#=================================================================================

import factory
from datetime import timedelta
from decimal import Decimal
from django.utils import timezone
from django.contrib.auth import get_user_model

from rentals.models import Booking, Listing

User = get_user_model()

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker("user_name")
    email = factory.LazyAttribute(lambda o: f"{o.username}@example.com")
    password = factory.PostGenerationMethodCall("set_password", "test123")

class ListingFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Listing

    title = factory.Faker("sentence", nb_words=4)
    description = factory.Faker("text", max_nb_chars=200)
    price = factory.LazyFunction(lambda: Decimal("75.00"))

class BookingFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Booking

    listing = factory.SubFactory(ListingFactory)
    user = factory.SubFactory(UserFactory)

    start_date = factory.LazyFunction(lambda: timezone.now().date() + timedelta(days=1))
    end_date = factory.LazyFunction(lambda: timezone.now().date() + timedelta(days=4))

    status = Booking.STATUS_PENDING
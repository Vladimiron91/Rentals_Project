from django.db.models import Q
from rest_framework import generics, permissions
from rest_framework.response import Response
from rentals.models import Listing, SearchQuery
from rentals.serializers import ListingSerializer


class ListingSearchView(generics.ListAPIView):
    """
    Поиск объявлений с сохранением запроса в историю.
    """
    serializer_class = ListingSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        queryset = Listing.objects.filter(is_active=True)

        # Получаем параметры поиска
        query = self.request.GET.get('q', '').strip()
        min_price = self.request.GET.get('min_price')
        max_price = self.request.GET.get('max_price')
        location = self.request.GET.get('location')
        rooms = self.request.GET.get('rooms')
        property_type = self.request.GET.get('property_type')

        # Поиск по ключевым словам
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(location__icontains=query)
            )
            # Сохраняем поисковый запрос
            self.save_search_query(query)

        # Фильтрация по цене
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)

        # Фильтрация по местоположению
        if location:
            queryset = queryset.filter(location__icontains=location)

        # Фильтрация по количеству комнат
        if rooms:
            queryset = queryset.filter(rooms=rooms)

        # Фильтрация по типу жилья
        if property_type:
            queryset = queryset.filter(property_type=property_type)

        # Сортировка
        sort_by = self.request.GET.get('sort_by', 'created_at')
        if sort_by in ['price', 'created_at', 'views_count']:
            order = self.request.GET.get('order', 'desc')
            prefix = '-' if order == 'desc' else ''
            queryset = queryset.order_by(f'{prefix}{sort_by}')

        return queryset

    def save_search_query(self, query):
        """Сохраняет поисковый запрос в историю"""
        user = self.request.user if self.request.user.is_authenticated else None
        search_query, created = SearchQuery.objects.get_or_create(
            query=query,
            user=user,
            defaults={'count': 1}
        )
        if not created:
            search_query.count += 1
            search_query.save(update_fields=['count'])

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        # Добавляем метаданные о поиске
        response.data = {
            'search_query': request.GET.get('q', ''),
            'results_count': len(response.data),
            'listings': response.data
        }
        return response
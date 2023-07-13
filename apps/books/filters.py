from django_filters import FilterSet, NumberFilter

from books.models import Book


class CustomFilter(FilterSet):
    year_to = NumberFilter(field_name='year_pub', lookup_expr='lte')
    year_from = NumberFilter(field_name='year_pub', lookup_expr='gte')

    class Meta:
        model = Book
        fields = ['category__name', 'price', 'year_from', 'year_to', 'author__name']

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListCreateAPIView
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.viewsets import ModelViewSet

from books.filters import CustomFilter
from books.models import Book, Author, Category, ViewCount
from books.serializer import BookModelSerializer, AuthorModelSerializer, CategoryModelSerializer


# files_params = openapi.Parameter('files', openapi.IN_FORM,
#                                  type=openapi.TYPE_ARRAY,
#                                  items=openapi.Items(type=openapi.TYPE_FILE),
#                                  required=True)


class BookModelViewSet(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookModelSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = CustomFilter
    search_fields = ['author__name', 'name', 'year_pub']
    parser_classes = FormParser, MultiPartParser

    def retrieve(self, request, *args, **kwargs):
        ViewCount.objects.get_or_create(book_id=kwargs.get('pk'), user=request.user)
        return super().retrieve(self, request, *args, **kwargs)


class AuthorListCreateAPIView(ListCreateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorModelSerializer


class CategoryListCreateAPIView(ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryModelSerializer

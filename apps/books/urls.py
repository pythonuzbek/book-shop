from django.urls import path, include
from rest_framework.routers import DefaultRouter

from books.views import BookModelViewSet, CategoryListCreateAPIView, AuthorListCreateAPIView

routers = DefaultRouter()
routers.register('books', BookModelViewSet, 'books')

urlpatterns = [
    path('', include(routers.urls)),
    path('category', CategoryListCreateAPIView.as_view(), name='category'),
    path('author', AuthorListCreateAPIView.as_view(), name='author')
]

from rest_framework.fields import IntegerField
from rest_framework.serializers import ModelSerializer

from books.models import Book, Author, Category, ViewCount


class BookModelSerializer(ModelSerializer):
    page_count = IntegerField(read_only=True)

    class Meta:
        model = Book
        fields = '__all__'

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['view_count'] = ViewCount.objects.filter(book_id=instance.id).count()
        return rep


class AuthorModelSerializer(ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'


class CategoryModelSerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

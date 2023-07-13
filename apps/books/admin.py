from django.contrib.admin import SimpleListFilter, ModelAdmin
from django.contrib import admin
from django.utils.safestring import mark_safe

from books.models import Book, Category, Author


class TopBooks(SimpleListFilter):
    title = 'Top Books'
    parameter_name = 'top_books'

    def lookups(self, request, model_admin):
        return [
            ("10", "top 10 books"),
            ("50", "top 50 books"),
            ("100", "top 100 books"),
        ]

    def queryset(self, request, queryset):
        if self.value() in ("10", "50", "100"):
            return queryset.order_by('-view_count')[0:int(self.value())]


@admin.register(Book)
class BookAdmin(ModelAdmin):
    list_display = ('name', 'category', 'author', 'get_pdf')
    # list_filter = TopBooks,
    search_fields = ('name', 'category__name', 'author__name')
    fields = ('title', 'category', 'author', 'pdf', 'year',)

    def get_pdf(self, obj: Book):
        return mark_safe(f'<a href="{obj.pdf.url}" target="_blank">Show Pdf</a>')


admin.site.register(Category)
admin.site.register(Author)

from django.urls import path, include

urlpatterns = [
    path('', include('books.urls')),
    path('users/', include('users.urls')),
]

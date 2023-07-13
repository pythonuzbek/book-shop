from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

from root import settings

schema_view = get_schema_view(
    openapi.Info(
        title="Book shop",
        default_version='v1',
        description="Book shop api",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
)

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('api/', include('apps.urls')),
                  path('', schema_view.with_ui('swagger', cache_timeout=0)),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

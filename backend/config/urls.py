"""config URL Configuration."""
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    path("", include("core.urls")),
    path("admin/", admin.site.urls),
    path("api/", include("core.urls")),
    # Favicon
    path("favicon.ico", RedirectView.as_view(url='/static/img/favicon.ico', permanent=True)),
]

# Servir archivos media en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/events/", include("event_api.urls", namespace="event_api")),
    path("__debug__/", include("debug_toolbar.urls")),
    path("api-auth/", include("rest_framework.urls")),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

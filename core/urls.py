from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.authtoken import views

urlpatterns = [
    path("auth/", include("drf_social_oauth2.urls", namespace="drf")),
    path("admin/", admin.site.urls),
    path("api/v1/events/", include("event.urls", namespace="event")),
    path("api/v1/accounts/", include("account.urls", namespace="account")),
    path("api/v1/accounts/", include("order.urls", namespace="order")),
    path("api/v1/pages/", include("page.urls", namespace="page")),
    path("__debug__/", include("debug_toolbar.urls")),
    path("api-auth/", include("rest_framework.urls")),
    path("api-token-auth/", views.obtain_auth_token),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "docs/",
        SpectacularSwaggerView.as_view(
            template_name="swagger-ui.html", url_name="schema"
        ),
        name="swagger-ui",
    ),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

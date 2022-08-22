from django.urls import path

from event_api.views import (
    BatchListCreate,
    BatchRetriveUpdateDelete,
    CategoryListCreate,
    CategoryRetrieveUpdate,
    EventListCreate,
    EventRetriveUpdate,
    EventByCategoriesList,
    LeasingListCreate,
)

app_name = "event_api"

urlpatterns = [
    path("events/", EventListCreate.as_view(), name="event-list"),
    path("events/<int:pk>/", EventRetriveUpdate.as_view(), name="event-retrieve"),
    path(
        "events/<int:event_pk>/batches/",
        BatchListCreate.as_view(),
    ),
    path(
        "events/<int:event_pk>/batches/<int:pk>/",
        BatchRetriveUpdateDelete.as_view(),
    ),
    path(
        "events/<int:event_pk>/leases/",
        LeasingListCreate.as_view(),
    ),
    path(
        "categories/",
        CategoryListCreate.as_view(),
        name="category-list-create",
    ),
    path(
        "categories/<int:pk>/",
        CategoryRetrieveUpdate.as_view(),
        name="category-retrieve-update",
    ),
    path(
        "categories/<int:pk>/events/",
        EventByCategoriesList.as_view(),
        name="category-event-list",
    ),
]

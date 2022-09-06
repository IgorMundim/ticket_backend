from django.urls import path

from event.views import (
    AddressListCreate,
    AddressRetrieveUpdateDestroy,
    BatchListCreate,
    BatchRetrieveUpdateDestroy,
    CategoryListCreate,
    CategoryRetrieveUpdate,
    EventByCategoriesList,
    EventListCreate,
    EventRetrieveUpdate,
    ImageListCreate,
    ImageRetrieveUpdateDestroy,
    LeasingListCreate,
    LeasingRetrieveUpdate,
)

app_name = "event"

urlpatterns = [
    path("", EventListCreate.as_view(), name="event-list-create"),
    path(
        "<int:pk>/",
        EventRetrieveUpdate.as_view(),
        name="event-retrieve-update",
    ),
    path(
        "<int:event_pk>/batches/",
        BatchListCreate.as_view(),
        name="batch-list-create",
    ),
    path(
        "batches/<int:pk>/",
        BatchRetrieveUpdateDestroy.as_view(),
        name="batch-retrieve-update",
    ),
    path(
        "<int:event_pk>/leases/",
        LeasingListCreate.as_view(),
        name="leasing-list-create",
    ),
    path(
        "leases/<int:pk>/",
        LeasingRetrieveUpdate.as_view(),
        name="leasing-retrieve-update",
    ),
    path(
        "categories/",
        CategoryListCreate.as_view(),
        name="categories-list-create",
    ),
    path(
        "categories/<int:pk>/",
        CategoryRetrieveUpdate.as_view(),
        name="category-retrieve-update",
    ),
    path(
        "categories/<int:pk>/events/",
        EventByCategoriesList.as_view(),
        name="events-by-category",
    ),
    path(
        "<int:event_pk>/adresses/",
        AddressListCreate.as_view(),
        name="address-list-create",
    ),
    path(
        "adresses/<int:pk>/",
        AddressRetrieveUpdateDestroy.as_view(),
        name="address-retrieve-update-destroy",
    ),
    path(
        "<int:event_pk>/images/",
        ImageListCreate.as_view(),
        name="image-list-create",
    ),
    path(
        "image/<int:pk>/",
        ImageRetrieveUpdateDestroy.as_view(),
        name="image-retrieve-update-destroy",
    ),
]

from django.urls import path

from event_api.views import (BatchListCreate, BatchRetrieveUpdateDestroy,
                             CategoryListCreate, CategoryRetrieveUpdate,
                             EventByCategoriesList, EventListCreate,
                             EventRetrieveUpdate, LeasingListCreate,
                             LeasingRetrieveUpdate, TicketListCreate)

app_name = "event_api"

urlpatterns = [
    path("", EventListCreate.as_view(), name="event-list"),
    path("<int:pk>/", EventRetrieveUpdate.as_view(), name="event-retrieve"),
    path(
        "<int:event_pk>/batches/",
        BatchListCreate.as_view(),
    ),
    path(
        "batches/<int:pk>/",
        BatchRetrieveUpdateDestroy.as_view(),
        name="batch-retrieve",
    ),
    path(
        "<int:event_pk>/leases/",
        LeasingListCreate.as_view(),
    ),
    path(
        "leases/<int:pk>/",
        LeasingRetrieveUpdate.as_view(),
        name="leasing-retrieve",
    ),
    path(
        "leases/<int:leasing_pk>/tickets/",
        TicketListCreate.as_view(),
    ),
    path(
        "categories/",
        CategoryListCreate.as_view(),
    ),
    path(
        "categories/<int:pk>/",
        CategoryRetrieveUpdate.as_view(),
        name="category-retrieve",
    ),
    path(
        "categories/<int:pk>/events/",
        EventByCategoriesList.as_view(),
        name="events-by-category",
    ),
]

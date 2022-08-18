from django.urls import path

from event_api.views import (
    CategoryListCreate,
    CategoryRetrieveUpdate,
    EventList,
    EventRetrive,
    EventsListByCategories,
    ListCreateBatck,
    RetriveUpdateBatck,
)

app_name = "event_api"

urlpatterns = [
    path("events/", EventList.as_view(), name="event-list"),
    path("events/<int:pk>/", EventRetrive.as_view(), name="event-retrieve"),
    path(
        "events/<int:pk>/batcks",
        ListCreateBatck.as_view(),
    ),
    path(
        "events/<int:event_pk>/batcks/<int:pk>",
        RetriveUpdateBatck.as_view(),
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
        EventsListByCategories.as_view(),
        name="category-event-list",
    ),
]

from django.urls import path

from account.views import (
    AccountCreate,
    AccountRetriveUpdate,
    AddressListCreate,
    AddressRetrieveUpdateDestroy,
    CustomerCreate,
    CustomerRetriveUpdate,
    ProducerCreate,
    ProducerRetriveUpdate,
)

app_name = "account"

urlpatterns = [
    path(
        "",
        AccountCreate.as_view(),
        name="account-create"
    ),
    path(
        "<int:pk>/",
        AccountRetriveUpdate.as_view(), 
        name="account-retrieve-update",
    ),
    path(
        "<int:pk>/addresses/",
        AddressListCreate.as_view(),
        name="address-list-create"
    ),
    path(
        "addresses/<int:pk>/",
        AddressRetrieveUpdateDestroy.as_view(),
        name="address-retrieve-update",
    ),
    path(
        "<int:pk>/customers/",
        CustomerCreate.as_view(),
        name="customer-create",
    ),
    path(
        "customers/<int:pk>/",
        CustomerRetriveUpdate.as_view(),
        name="customer-retrieve-update",
    ),
    path(
        "<int:pk>/producers/",
        ProducerCreate.as_view(),
        name="producer-create",
    ),
    path(
        "producers/<int:pk>/",
        ProducerRetriveUpdate.as_view(),
        name="producer-retrieve-update",
    ),
]

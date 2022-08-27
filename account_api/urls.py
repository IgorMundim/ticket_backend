from django.urls import include, path

from account_api.views import (
    AccountCreate,
    AccountRetriveUpdate,
    AddressListCreate,
    AddressRetrieveUpdateDestroy,
    CustomerCreate,
    CustomerRetriveUpdate,
    ProducerCreate,
    ProducerRetriveUpdate,
    RequisitionListCreate,
    RequisitionRetriveUpdate,
)

app_name = "account_api"

urlpatterns = [
    path(
        "",
        AccountCreate.as_view(),
    ),
    path(
        "<int:pk>/",
        AccountRetriveUpdate.as_view(), 
        name="account-retrive",
    ),
    path(
        "<int:pk>/requisitions/",
        RequisitionListCreate.as_view(),
    ),
    path(
        "requisitions/<int:pk>/",
        RequisitionRetriveUpdate.as_view(),
        name="requisition-retrive"
    ),
    path(
        "<int:pk>/addresses/",
        AddressListCreate.as_view(),
    ),
    path(
        "addresses/<int:pk>/",
        AddressRetrieveUpdateDestroy.as_view(),
        name="address-retrive",
    ),
    path(
        "<int:pk>/customers/",
        CustomerCreate.as_view(),
    ),
    path(
        "customers/<int:pk>/",
        CustomerRetriveUpdate.as_view(),
        name="customer-retrive",
    ),
    path(
        "<int:pk>/producers/",
        ProducerCreate.as_view(),
    ),
    path(
        "producers/<int:pk>/",
        ProducerRetriveUpdate.as_view(),
        name="producer-retrive",
    ),
]

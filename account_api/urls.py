from django.urls import include, path

from account_api.views import (
    AccountCreate,
    AccountRetriveUpdate,
    AddressListCreate,
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
        "<int:account_pk>/",
        AccountRetriveUpdate.as_view(),
    ),
    path(
        "<int:account_pk>/requisitions/",
        RequisitionListCreate.as_view(),
    ),
    path(
        "<int:account_pk>/requisitions/<int:pk>/",
        RequisitionRetriveUpdate.as_view(),
    ),
    path(
        "<int:account_pk>/addresses/",
        AddressListCreate.as_view(),
    ),
]

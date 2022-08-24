from django.urls import include, path

from account_api.views import RequisitionListCreate, RequisitionRetriveUpdate

app_name = "account_api"

urlpatterns = [
    path(
        "requisition/",
        RequisitionListCreate.as_view(),
    ),
    path(
        "requisition/<int:pk>/",
        RequisitionRetriveUpdate.as_view(),
    ),
]

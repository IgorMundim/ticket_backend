from django.shortcuts import get_object_or_404
from account.models import Account, Address, Requisition
from rest_framework import generics
from rest_framework.permissions import SAFE_METHODS, AllowAny, BasePermission

from account_api.serializers import (
    AccountSerializer,
    AddressSerializer,
    RequisitionSerializer,
)


class IsOwner(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and view.kwargs["account_pk"] == request.user.id
        )


# class IsOwner(BasePermission):
#     def has_permission(self, request, view):
#         return super().has_permission(request, view)

#     def has_object_permission(self, request, view, obj):
#         return bool(request.user and obj == request.user)


class AccountCreate(generics.CreateAPIView, AllowAny):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [AllowAny]


class AccountRetriveUpdate(generics.RetrieveUpdateAPIView, IsOwner):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    # permission_classes = [IsOwner]

    def get_object(self):
        pk = self.kwargs.get("account_pk")
        obj = get_object_or_404(
            self.get_queryset(),
            pk=pk,
        )
        self.check_object_permissions(self.request, obj)
        return obj

class AddressListCreate(generics.ListCreateAPIView):
    queryset = Address
    serializer_class = AddressSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.objects.filter(account=self.kwargs.get("account_pk"))
        return qs


class RequisitionListCreate(generics.ListCreateAPIView):
    queryset = Requisition.objects.all()
    serializer_class = RequisitionSerializer

    def get_queryset(self):
        qs = self.queryset.objects.filter(
            account=self.kwargs.get("account_pk")
        )
        return qs


class RequisitionRetriveUpdate(generics.RetrieveUpdateAPIView, IsOwner):
    queryset = Requisition
    serializer_class = RequisitionSerializer
    permission_classes = [IsOwner]

    def get_queryset(self):
        qs = self.queryset.objects.filter(
            account=self.kwargs.get("account_pk")
        )
        return qs

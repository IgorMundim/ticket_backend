from account.models import Account, Address, Customer, Producer, Requisition
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.permissions import SAFE_METHODS, AllowAny, BasePermission

from account_api.serializers import (
    AccountSerializer,
    AddressSerializer,
    CustomerSerializer,
    ProducerSerializer,
    RequisitionSerializer,
)


class IsOwnerObject(BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(request.user and obj.account == request.user)


class IsOwner(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and view.kwargs["pk"] == request.user.id)


class AccountCreate(generics.CreateAPIView, AllowAny):
    queryset = Account.objects.filter(is_active=True)
    serializer_class = AccountSerializer
    permission_classes = [AllowAny]


class AccountRetriveUpdate(generics.RetrieveUpdateAPIView, IsOwner):
    queryset = Account.objects.filter(is_active=True)
    serializer_class = AccountSerializer
    permission_classes = [IsOwner]


class AddressListCreate(generics.ListCreateAPIView, IsOwner):
    queryset = Address
    serializer_class = AddressSerializer
    permission_classes = [IsOwner]

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.objects.filter(account=self.kwargs.get("pk"))
        return qs


class AddressRetrieveUpdateDestroy(
    generics.RetrieveUpdateDestroyAPIView, IsOwnerObject
):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    permission_classes = [IsOwnerObject]


class RequisitionListCreate(generics.ListCreateAPIView, IsOwner):
    queryset = Requisition
    serializer_class = RequisitionSerializer
    permission_classes = [IsOwner]

    def get_queryset(self):
        qs = self.queryset.objects.filter(account=self.kwargs.get("pk"))
        return qs


class RequisitionRetriveUpdate(generics.RetrieveUpdateAPIView, IsOwnerObject):
    queryset = Requisition.objects.all()
    serializer_class = RequisitionSerializer
    permission_classes = [IsOwnerObject]


class ProducerCreate(generics.CreateAPIView, IsOwner):
    queryset = Producer.objects.all()
    serializer_class = ProducerSerializer
    permission_classes = [IsOwner]


class ProducerRetriveUpdate(generics.RetrieveUpdateAPIView, IsOwnerObject):
    queryset = Producer.objects.all()
    serializer_class = ProducerSerializer
    permission_classes = [IsOwnerObject]


class CustomerCreate(generics.CreateAPIView, IsOwner):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsOwner]


class CustomerRetriveUpdate(generics.RetrieveUpdateAPIView, IsOwnerObject):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsOwnerObject]

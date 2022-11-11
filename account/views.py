from django.http import Http404
from rest_framework import generics, permissions, status
from rest_framework.permissions import AllowAny, BasePermission
from rest_framework.response import Response
from rest_framework.views import APIView

from account.models import Account, Address, Customer, Producer
from account.serializers import (
    AccountSerializer,
    AddressSerializer,
    CustomerPostSerializer,
    CustomerSerializer,
    ProducerSerializer,
    UsersSerializer,
)


class IsOwnerObject(BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(request.user and obj.account == request.user)


class IsOwner(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and view.kwargs["pk"] == request.user.id)


class CurrentUser(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        serializer = UsersSerializer(self.request.user)
        return Response(serializer.data)


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


class ProducerCreate(generics.CreateAPIView, IsOwner):
    queryset = Producer.objects.all()
    serializer_class = ProducerSerializer
    permission_classes = [IsOwner]


class ProducerRetriveUpdate(generics.RetrieveUpdateAPIView, IsOwnerObject):
    queryset = Producer.objects.all()
    serializer_class = ProducerSerializer
    permission_classes = [IsOwnerObject]


class CustomerCreate(APIView, IsOwner):
    permission_classes = [IsOwner]

    def get_object(self, pk):
        try:
            return Customer.objects.get(account=pk)
        except Customer.DoesNotExist:
            raise Http404

    def post(self, request, pk, format=None):
        serializer = CustomerPostSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk, format=None):
        costumer = self.get_object(pk)
        serializer = CustomerSerializer(costumer, context={"request": request})
        return Response(serializer.data)


class CustomerRetriveUpdate(generics.RetrieveUpdateAPIView, IsOwnerObject):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsOwnerObject]

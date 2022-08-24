from account.models import Requisition
from rest_framework import generics
from rest_framework.permissions import SAFE_METHODS, BasePermission, IsAuthenticated

from account_api.serializers import RequisitionSerializer


class IsOwner(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        objectOwner = Requisition.objects.filter(account=request.data["account"]).first()
        return bool(objectOwner and request.user and objectOwner.account == request.user)
        
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return bool(request.user and obj.account == request.user)

class RequisitionListCreate(generics.ListCreateAPIView, IsOwner):
    queryset = Requisition.objects.all()
    serializer_class = RequisitionSerializer
    permission_classes = [IsOwner]

class RequisitionRetriveUpdate(generics.RetrieveUpdateAPIView, IsOwner):
    queryset = Requisition.objects.all()
    serializer_class = RequisitionSerializer
    permission_classes = [IsOwner]


from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.permissions import (
    SAFE_METHODS,
    BasePermission,
    IsAuthenticatedOrReadOnly,
)
from rest_framework.response import Response
from rest_framework.views import APIView

from event.models import Address, Batch, Category, Event, Image, Leasing

from .serializers import (
    AddressSerializer,
    BasicEventSerializer,
    BatchSerializers,
    CategorySerializer,
    EventCreateSerializer,
    EventSerializer,
    ImageSerializer,
    LeasingSerializer,
)


class IsSuperUser(BasePermission):
    # message = "Editing posts is restricted to the author only."
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:

            return True
        return bool(request.user and request.user.is_superuser)


class IsOwnerEvent(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return bool(request.user and obj.account == request.user)


class IsOwner(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        owner = (
            Event.objects.filter(pk=view.kwargs["event_pk"])
            .select_related("account")
            .values("account")
            .first()
        )
        return bool(owner is not None and owner["account"] == request.user.id)


class IsOwnerObject(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return bool(
            obj.event.account_id is not None
            and obj.event.account_id == request.user.id
        )


class CategoryListCreate(generics.ListCreateAPIView, IsSuperUser):
    permission_classes = [IsSuperUser]
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer


class CategoryRetrieveUpdate(generics.RetrieveUpdateAPIView, IsSuperUser):
    permission_classes = [IsSuperUser]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class EventByCategoriesList(generics.ListAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(categories=self.kwargs.get("pk")).select_related(
            "address", "image"
        )
        return qs


class EventListCreate(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, format=None):
        events = (
            Event.objects.get_event()
            .select_related("image", "address", "account")
            .prefetch_related("categories")
        )
        serializer = EventSerializer(
            events, many=True, context={"request": None}
        )
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = EventCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class EventRetrieveUpdate(generics.RetrieveUpdateAPIView, IsOwnerEvent):
    queryset = (
        Event.objects.get_event()
        .select_related("image", "address", "account")
        .prefetch_related("categories")
    )
    serializer_class = EventSerializer
    permission_classes = [IsOwnerEvent]


class BatchListCreate(generics.ListCreateAPIView, IsOwner):
    queryset = Batch
    serializer_class = BatchSerializers
    permission_classes = [IsOwner]

    def get_queryset(self):
        return self.queryset.objects.filter(event=self.kwargs.get("event_pk"))


class BatchRetrieveUpdateDestroy(
    generics.RetrieveUpdateDestroyAPIView, IsOwnerObject
):
    queryset = Batch.objects.all()
    serializer_class = BatchSerializers
    permission_classes = [IsOwnerObject]


class LeasingListCreate(generics.ListCreateAPIView, IsOwner):
    queryset = Leasing
    serializer_class = LeasingSerializer
    permission_classes = [IsOwner]

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.objects.get_leasing(event_pk=self.kwargs.get("event_pk"))
        return qs


class LeasingRetrieveUpdate(generics.RetrieveUpdateAPIView, IsOwnerObject):
    queryset = Leasing
    serializer_class = LeasingSerializer
    permission_classes = [IsOwnerObject]


class AddressListCreate(generics.ListCreateAPIView, IsOwner):
    queryset = Address
    serializer_class = AddressSerializer
    permission_classes = [IsOwner]

    def get_queryset(self):
        return self.queryset.objects.filter(event=self.kwargs.get("event_pk"))


class AddressRetrieveUpdateDestroy(
    generics.RetrieveUpdateDestroyAPIView, IsOwnerObject
):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    permission_classes = [IsOwnerObject]


class ImageListCreate(generics.ListCreateAPIView, IsOwner):
    queryset = Image
    serializer_class = ImageSerializer
    permission_classes = [IsOwner]

    def get_queryset(self):
        return self.queryset.objects.filter(event=self.kwargs.get("event_pk"))


class ImageRetrieveUpdateDestroy(
    generics.RetrieveUpdateDestroyAPIView, IsOwnerObject
):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    permission_classes = [IsOwnerObject]

from customer.models import Producer
from django.shortcuts import get_object_or_404
from event.models import Batck, Category, Event
from rest_framework import generics
from rest_framework.permissions import (
    SAFE_METHODS,
    BasePermission,
    IsAuthenticatedOrReadOnly,
)

from .serializers import (
    AddressSerializer,
    BasicEventSerializer,
    BatckSerializers,
    CategorySerializer,
    EventSerializer,
)


class IsSuperUser(BasePermission):
    # message = "Editing posts is restricted to the author only."
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:

            return True
        return bool(request.user and request.user.is_superuser)


class IsOwnerUser(BasePermission):
    def has_object_permission(self, request, view, obj):
        print(request.method)
        if request.method in SAFE_METHODS:
            return True

        return bool(request.user and obj.producer.account == request.user)


class IsOwnerBatck(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        owner = (
            Event.objects.filter(pk=obj.event_id)
            .select_related("producer")
            .values("producer")
            .first()
        )
        user = (
            Producer.objects.filter(pk=request.user.id)
            .select_related("account")
            .values("id")
            .first()
        )

        return bool(
            user is not None
            and owner is not None
            and user["id"] == owner["producer"]
        )


class CategoryListCreate(generics.ListCreateAPIView, IsSuperUser):
    permission_classes = [IsSuperUser]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryRetrieveUpdate(generics.RetrieveUpdateAPIView, IsSuperUser):
    permission_classes = [IsSuperUser]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class EventsListByCategories(generics.ListAPIView):
    queryset = Event.objects.all()
    serializer_class = BasicEventSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(categories=self.kwargs.get("pk")).select_related(
            "address", "image"
        )
        return qs

    def get_object(self):
        obj = get_object_or_404(self.get_queryset())
        return obj


class EventList(
    generics.ListCreateAPIView,
):
    queryset = (
        Event.objects.get_event()
        .select_related("producer", "image", "address")
        .prefetch_related("categories")
    )

    serializer_class = EventSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class EventRetrive(generics.RetrieveUpdateAPIView, IsOwnerUser):
    queryset = Event.objects.get_event()

    serializer_class = EventSerializer
    permission_classes = [IsOwnerUser]


class ListCreateBatck(generics.ListCreateAPIView):
    queryset = Batck.objects.all()
    serializer_class = BatckSerializers


class RetriveUpdateBatck(generics.RetrieveUpdateAPIView, IsOwnerBatck):
    queryset = Batck.objects.all()
    serializer_class = BatckSerializers
    permission_classes = [IsOwnerBatck]

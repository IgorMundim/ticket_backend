from account.models import Producer, Requisition
from django.shortcuts import get_object_or_404
from event.models import Batch, Category, Event, Leasing, Ticket
from rest_framework import generics
from rest_framework.permissions import (
    SAFE_METHODS,
    BasePermission,
    IsAuthenticatedOrReadOnly,
)

from .serializers import (
    AddressSerializer,
    BasicEventSerializer,
    BatchSerializers,
    CategorySerializer,
    EventSerializer,
    LeasingSerializer,
    TicketSerializer,
)


class IsSuperUser(BasePermission):
    # message = "Editing posts is restricted to the author only."
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:

            return True
        return bool(request.user and request.user.is_superuser)


class IsOwnerUser(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        return bool(request.user and obj.producer.account == request.user)


class IsOwnerEvent(BasePermission):
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
        print(user["id"])
        print(request.user.id)
        return bool(
            user is not None
            and owner is not None
            and user["id"] == owner["producer"]
        )

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        owner = (
            Event.objects.filter(pk=view.kwargs["event_pk"])
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


class IsOwnerTicket(BasePermission):
    def has_object_permission(self, request, view, obj):
        return False

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        owner = (
            Requisition.objects.filter(id=request.data["requisition"])
            .values("account")
            .first()
        )

        return bool(
            owner["account"]
            and request.user.id
            and owner["account"] == request.user.id
        )


class CategoryListCreate(generics.ListCreateAPIView, IsSuperUser):
    permission_classes = [IsSuperUser]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryRetrieveUpdate(generics.RetrieveUpdateAPIView, IsSuperUser):
    permission_classes = [IsSuperUser]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class EventByCategoriesList(generics.ListAPIView):
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


class EventListCreate(
    generics.ListCreateAPIView,
):
    queryset = (
        Event.objects.get_event()
        .select_related("image", "address")
        .prefetch_related("categories")
    )

    serializer_class = EventSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class EventRetriveUpdate(generics.RetrieveUpdateAPIView, IsOwnerUser):
    queryset = (
        Event.objects.get_event()
        .select_related("image", "address")
        .prefetch_related("categories")
    )
    serializer_class = EventSerializer
    permission_classes = [IsOwnerUser]


class BatchListCreate(generics.ListCreateAPIView, IsOwnerEvent):
    queryset = Batch
    serializer_class = BatchSerializers
    permission_classes = [IsOwnerEvent]

    def get_queryset(self):
        return self.queryset.objects.filter(event=self.kwargs.get("event_pk"))


class BatchRetriveUpdateDelete(
    generics.RetrieveUpdateDestroyAPIView, IsOwnerEvent
):
    queryset = Batch
    serializer_class = BatchSerializers
    permission_classes = [IsOwnerEvent]

    def get_queryset(self):
        return self.queryset.objects.filter(event=self.kwargs.get("event_pk"))


class LeasingListCreate(generics.ListCreateAPIView, IsOwnerEvent):
    queryset = Leasing
    serializer_class = LeasingSerializer
    permission_classes = [IsOwnerEvent]

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.objects.get_leasing(event_pk=self.kwargs.get("event_pk"))
        return qs


class LeasingRetriveUpdate(generics.RetrieveUpdateAPIView, IsOwnerEvent):
    queryset = Leasing
    serializer_class = LeasingSerializer
    permission_classes = [IsOwnerEvent]

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.objects.get_leasing(event_pk=self.kwargs.get("event_pk"))
        return qs


class TicketListCreate(generics.ListCreateAPIView, IsOwnerTicket):
    queryset = Ticket.objects.all().select_related("leasing", "requisition")
    serializer_class = TicketSerializer
    permission_classes = [IsOwnerTicket]

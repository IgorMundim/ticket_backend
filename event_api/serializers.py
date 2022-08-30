from dataclasses import fields
from urllib import request

from event.models import (
    Address,
    Batch,
    Category,
    Event,
    Image,
    Leasing,
    Ticket,
)
from rest_framework import serializers


class CategorySerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="event_api:category-retrieve"
    )
    url_events = serializers.HyperlinkedIdentityField(
        view_name="event_api:events-by-category"
    )

    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "slug",
            "image_url",
            "alt_text",
            "url",
            "url_events",
        ]  # "image_url","alt_text"


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = [
            "id",
            "cep",
            "complement",
            "city",
            "district",
            "number",
            "roud",
            "state",
            "uf",
        ]


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ["id", "image_url", "alt_text"]


class BasicEventSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="event_api:event-retrieve"
    )
    address = serializers.StringRelatedField()
    image = serializers.StringRelatedField()
    # event_url = serializers.HyperlinkedRelatedField(
    #     many=False,
    #     view_name="event_api:event-retrieve",
    #     read_only=True,
    #     source="id",
    # )

    class Meta:
        model = Event
        fields = [
            "id",
            "name",
            "address",
            "image",
            "url",
        ]


class EventSerializer(serializers.ModelSerializer):

    # address = serializers.SlugRelatedField(
    #     many=False, read_only=True, slug_field="cep"
    # )
    # image = serializers.StringRelatedField()
    # producer = serializers.StringRelatedField()
    url = serializers.HyperlinkedIdentityField(
        view_name="event_api:event-retrieve"
    )
    address = AddressSerializer(many=False)
    # producer = ProducerSerializer(many=False)
    image = ImageSerializer(many=False)
    categories = CategorySerializer(many=True)

    class Meta:
        model = Event
        fields = [
            "id",
            "name",
            "in_room",
            "date_end",
            "date_start",
            "description",
            "is_virtual",
            "video_url",
            "is_published",
            "address",
            "account",
            "image",
            "categories",
            "url",
        ]


class BatchSerializers(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="event_api:batch-retrieve"
    )

    class Meta:
        model = Batch
        fields = [
            "id",
            "event",
            "percentage",
            "sales_qtd",
            "batch_stop_date",
            "description",
            "is_active",
            "url",
        ]

    def validate(self, attrs):
        sales_qtd = attrs.get("sales_qtd")
        batch_stop_date = attrs.get("batch_stop_date")

        if self._context["request"]._stream.method == "POST":

            batch = Batch.objects.filter_by_saler(
                event_pk=self.initial_data["event"],
                sales_qtd=sales_qtd,
                batch_stop_date=batch_stop_date,
            )
            if batch is not None:
                raise serializers.ValidationError("ERROR")
            return super().validate(attrs)

        event_pk = self.initial_data["event"]

        id = self.instance.id
        if not Batch.objects.is_valid_change(
            id=id,
            sales_qtd=sales_qtd,
            batch_stop_date=batch_stop_date,
            event_pk=event_pk,
        ):
            raise serializers.ValidationError("ERROR")

        return super().validate(attrs)


class LeasingSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="event_api:leasing-retrieve"
    )

    class Meta:
        model = Leasing
        fields = [
            "id",
            "event",
            "name",
            "descroption",
            "store_price",
            "sale_price",
            "student_price",
            "units_solid",
            "units",
            "is_active",
            "url",
        ]


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = [
            "id",
            "sale_price",
            "code",
            "is_student",
            "is_active",
            "requisition",
            "leasing",
        ]

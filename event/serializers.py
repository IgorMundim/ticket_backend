from rest_framework import serializers

from event.models import Address, Batch, Category, Event, Image, Leasing


class CategorySerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="event:category-retrieve-update"
    )
    url_events = serializers.HyperlinkedIdentityField(
        view_name="event:events-by-category"
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
            "zipcode",
            "complement",
            "city",
            "neighborhood",
            "number",
            "street",
            "uf",
        ]


class ImageSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="event:image-retrieve-update-destroy"
    )

    class Meta:
        model = Image
        fields = ["id", "event", "image_url", "alt_text", "url"]


class BasicEventSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="event:event-retrieve-update"
    )
    address = serializers.StringRelatedField()
    image = serializers.StringRelatedField()


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

    url = serializers.HyperlinkedIdentityField(
        view_name="event:event-retrieve-update"
    )
    address = AddressSerializer(many=False)
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


class EventCreateSerializer(serializers.ModelSerializer):
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
        ]


class BatchSerializers(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="event:batch-retrieve-update"
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
                raise serializers.ValidationError(
                    "Conflict between created lots"
                )
            return super().validate(attrs)

        if self._context["request"]._stream.method == "PATCH":
            raise serializers.ValidationError("Method is not allowed")
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
        view_name="event:leasing-retrieve-update"
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

        read_only_fields = ["sale_price", "student_price", "units_solid"]

    def validate_units(self, value):
        if self._context["request"]._stream.method != "POST":
            leasing = Leasing.objects.filter(
                id=self._context["request"].parser_context["kwargs"]["pk"]
            ).first()
            if value < leasing.units_solid:
                raise serializers.ValidationError(
                    "Units sold is greater than the quantity available."
                )
        return value


from customer.models import Producer
from event.models import Address, Batck, Category, Event, Image, TicketLeasing
from rest_framework import serializers


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "slug",
            "image_url",
            "alt_text",
        ]  # "image_url","alt_text"


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = [
            "cep",
            "complement",
            "city",
            "district",
            "number",
            "roud",
            "state",
            "uf",
        ]


class ProducerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producer
        fields = "__all__"


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ["image_url", "alt_text"]


class BasicEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = [
            "name",
            "address",
            "image",
            "event_url",
        ]

    address = serializers.StringRelatedField()
    image = serializers.StringRelatedField()
    event_url = serializers.HyperlinkedRelatedField(
        many=False,
        view_name="event_api:event-retrieve",
        read_only=True,
        source="id",
    )


class EventSerializer(serializers.ModelSerializer):

    # address = serializers.SlugRelatedField(
    #     many=False, read_only=True, slug_field="cep"
    # )
    # image = serializers.StringRelatedField()
    # producer = serializers.StringRelatedField()

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
            "producer",
            "image",
            "categories",
        ]

    address = AddressSerializer(many=False)
    producer = ProducerSerializer(many=False)
    image = ImageSerializer(many=False)
    categories = CategorySerializer(many=True)


class BatckSerializers(serializers.ModelSerializer):
    class Meta:
        model = Batck
        fields = [
            "id",
            "event",
            "sequence",
            "percentage",
            "sales_qtd",
            "batck_start_date",
            "batck_stop_date",
            "description",
            "is_active",
        ]

    def validate(self, attrs):
        sales_qtd = attrs.get("sales_qtd")
        batch_stop_date = attrs.get("batck_stop_date")
        event_pk = self.initial_data["event"]
        if self._context["request"]._stream.method is not "POST":

            batch = Batck.objects.filter_by_saler(
                event_pk=self.initial_data["event"],
                sales_qtd=sales_qtd,
                batck_stop_date=batch_stop_date,
            )
            if batch is not None:
                raise serializers.ValidationError("ERROR")
            return super().validate(attrs)
            
        id = self.instance.id
        if not Batck.objects.is_valid_change(
            id=id,
            sales_qtd=sales_qtd,
            batch_stop_date=batch_stop_date,
            event_pk=event_pk,
        ):
            raise serializers.ValidationError("ERROR")

        return super().validate(attrs)


class TicketLeasingSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketLeasing
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
        ]

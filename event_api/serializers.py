from customer.models import Producer
from event.models import Address, Batck, Category, Event, Image
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
            "municipality_IBGE",
            "number",
            "roud",
            "state",
            "uf",
            "uf_ibge",
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
            "event",
            "sequence",
            "sales_qtd",
            "batck_start_date",
            "batck_stop_date",
            "description",
            "is_active",
        ]

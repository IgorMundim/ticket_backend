from django.contrib.auth import get_user_model
from rest_framework import serializers

from account.models import Account, Address, Customer, Producer, Requisition
from utils.validation import strong_password


class RequisitionSerializer(serializers.ModelSerializer):
    is_paid = serializers.StringRelatedField(read_only=True)
    url = serializers.HyperlinkedIdentityField(
        view_name="account_api:requisition-retrive",
    )

    class Meta:
        model = Requisition
        fields = [
            "id",
            "date_joined",
            "is_paid",
            "type_of_payment",
            "account",
            "url",
        ]


class AccountSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True, required=True)
    url = serializers.HyperlinkedIdentityField(
        view_name="account_api:account-retrive",
    )

    class Meta:
        model = Account
        fields = [
            "id",
            "username",
            "email",
            "profile_image",
            "is_active",
            "password",
            "password2",
            "url",
        ]
        extra_kwargs = {"password": {"write_only": True, "min_length": 8}}

    def validate(self, attrs):
        strong_password(attrs["password"])
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )
        return attrs

    def create(self, validated_data):
        account = Account.objects.create(
            validated_data["email"],
            validated_data["username"],
            validated_data.get("profile_image",""),
            validated_data["password"],
        )
        return account

    def update(self, instance, validated_data):
        instance.username = validated_data.get("username", instance.username)
        instance.email = validated_data.get("email", instance.email)
        instance.is_active = validated_data.get(
            "is_active", instance.is_active
        )
        instance.profile_image = validated_data.get(
            "profile_image", instance.profile_image
        )
        instance.set_password(
            validated_data.get("password", instance.password)
        )
        instance.save()
        return instance


class AddressSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="account_api:address-retrive",
    )

    class Meta:
        model = Address
        fields = [
            "id",
            "account",
            "telephone",
            "cep",
            "complement",
            "city",
            "district",
            "number",
            "roud",
            "state",
            "uf",
            "types",
            "url",
        ]


class ProducerSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="account_api:producer-retrive",
    )

    class Meta:
        model = Producer
        fields = [
            "id",
            "account",
            "business_name",
            "cnpj",
            "fantasy_name",
            "state_registration",
            "municype_registration",
            "url",
        ]


class CustomerSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="account_api:customer-retrive",
    )

    class Meta:
        model = Customer
        fields = [
            "id",
            "account",
            "first_name",
            "last_name",
            "cpf",
            "britday",
            "url",
        ]

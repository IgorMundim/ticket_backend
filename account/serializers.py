from rest_framework import serializers

from account.models import Account, Address, Customer, Producer
from utils.validation import strong_password


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ["id"]


class AccountSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True, required=True)
    url = serializers.HyperlinkedIdentityField(
        view_name="account:account-retrieve-update",
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

    def validate_password(self, value):
        strong_password(value)
        return value

    def validate(self, attrs):
        if (
            attrs.get("password", False)
            and attrs["password"] != attrs["password2"]
        ):
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )
        return attrs

    def create(self, validated_data):

        account = Account.objects.create_user(
            validated_data["email"],
            validated_data["username"],
            validated_data["password"],
            validated_data.get("profile_image", ""),
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
        view_name="account:address-retrieve-update",
    )

    class Meta:
        model = Address
        fields = [
            "id",
            "account",
            "telephone",
            "zipcode",
            "complement",
            "city",
            "neighborhood",
            "number",
            "street",
            "uf",
            "types",
            "url",
        ]


class ProducerSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="account:producer-retrieve-update",
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
        view_name="account:customer-retrieve-update",
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


class CustomerPostSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="account:customer-retrieve-update",
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

    def validate_account(self, value):
        if str(value.id) != str(
            self._context["request"].parser_context["kwargs"]["pk"]
        ):
            raise serializers.ValidationError("Account Invalid")
        return value

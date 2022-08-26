from dataclasses import fields
from account.models import Account, Address, Requisition
from django.contrib.auth import get_user_model
from rest_framework import serializers


class RequisitionSerializer(serializers.ModelSerializer):
    is_paid = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Requisition
        fields = [
            "id",
            "date_joined",
            "is_paid",
            "type_of_payment",
            "account",
        ]




class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = [
        
            "username",
            "email", 
            "profile_image",
            # "is_active",
            "password",
        ]

    # last_login = serializers.StringRelatedField(read_only=True)
    # date_joined = serializers.StringRelatedField(read_only=True)
    # is_superuser = serializers.StringRelatedField(read_only=True)
    # is_admin = serializers.StringRelatedField(read_only=True)

    def create(self, validated_data):
        account = Account.objects.create_customer(validated_data["email"], validated_data["username"], validated_data["profile_image"], validated_data["password"] )
        return account
    
    def update(self, instance, validated_data):
        instance.username = validated_data.get("username", instance.username)
        instance.email = validated_data.get("email", instance.email)
        instance.profile_image = validated_data.get("profile_image", instance.profile_image)
        instance.set_password(validated_data.get("password",instance.password))
        instance.save()
        return instance

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = [
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
        ]
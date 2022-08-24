from account.models import Requisition
from rest_framework import serializers


class RequisitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Requisition
        fields = [
        "id",
		"date_joined",
		"is_paid",
		"type_of_payment",
		"account",
        ]

    is_paid = serializers.StringRelatedField(read_only=True)

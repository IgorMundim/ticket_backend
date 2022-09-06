# class RequisitionSerializer(serializers.ModelSerializer):
#     is_paid = serializers.StringRelatedField(read_only=True)
#     url = serializers.HyperlinkedIdentityField(
#         view_name="account:requisition-retrive",
#     )

#     class Meta:
#         model = Requisition
#         fields = [
#             "id",
#             "date_joined",
#             "is_paid",
#             "type_of_payment",
#             "account",
#             "url",
#         ]
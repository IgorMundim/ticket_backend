from django.shortcuts import render

# class RequisitionListCreate(generics.ListCreateAPIView, IsOwner):
#     queryset = Requisition
#     serializer_class = RequisitionSerializer
#     permission_classes = [IsOwner]

#     def get_queryset(self):
#         qs = self.queryset.objects.filter(account=self.kwargs.get("pk"))
#         return qs


# class RequisitionRetriveUpdate(generics.RetrieveUpdateAPIView, IsOwnerObject):
#     queryset = Requisition.objects.all()
#     serializer_class = RequisitionSerializer
#     permission_classes = [IsOwnerObject]
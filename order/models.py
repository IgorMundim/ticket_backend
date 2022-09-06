from django.db import models
from event.models import Leasing
from account.models import Account

class Order(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    date_joined = models.DateTimeField(
        verbose_name="date joined", auto_now_add=True, editable=False
    )
    is_paid = models.BooleanField(default=False)
    type_of_payment = models.DecimalField(
        verbose_name="type of payment", max_digits=2, decimal_places=0
    )

    class Meta:
        verbose_name = "requisition"
        verbose_name_plural = "requisitions"

class Ticket(models.Model):
    requisition = models.ForeignKey(Order, on_delete=models.PROTECT)
    leasing = models.ForeignKey(Leasing, on_delete=models.CASCADE)
    sale_price = models.DecimalField(
        verbose_name="sale price", max_digits=8, decimal_places=2
    )
    code = models.CharField(max_length=255)
    is_student = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = "ticket"
        verbose_name_plural = "tickets"
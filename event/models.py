from typing import Any

from django.db import models
from django.db.models import Q
from django.utils import timezone

from account.models import Account


class Address(models.Model):
    zipcode = models.CharField(max_length=8)
    complement = models.CharField(max_length=150)
    city = models.CharField(max_length=100)
    neighborhood = models.CharField(max_length=100)
    number = models.IntegerField()
    street = models.CharField(max_length=100)
    uf = models.CharField(max_length=2)

    def __str__(self):
        return "%s - %s" % (self.city, self.uf)

    class Meta:
        verbose_name = "address"
        verbose_name_plural = "adresses"


class Image(models.Model):
    image_url = models.ImageField(
        max_length=200,
        upload_to="covers/%Y/%m/%d/",
        blank=True,
    )
    alt_text = models.CharField(max_length=150)

    def __str__(self):
        return "%s" % (self.image_url)

    class Meta:
        verbose_name = "image"
        verbose_name_plural = "images"


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True)
    image_url = models.ImageField(
        max_length=200,
        upload_to="covers/%Y/%m/%d/",
        blank=True,
    )
    alt_text = models.CharField(max_length=150)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        verbose_name = "category"
        verbose_name_plural = "categories"


class EventManager(models.Manager):
    def get_event(self):
        return (
            self.filter(is_published=True).order_by("-id")
            # .select_related("producer", "address")
        )


class Event(models.Model):
    objects = EventManager()
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    address = models.OneToOneField(
        Address,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        )

    categories = models.ManyToManyField(Category, blank=True, null=True)
    image = models.OneToOneField(Image, on_delete=models.PROTECT, blank=True, null=True)
    name = models.CharField(max_length=100)
    in_room = models.BooleanField(verbose_name="in room", default=True)
    date_end = models.DateTimeField(verbose_name="date end")
    date_start = models.DateTimeField(verbose_name="date start")
    description = models.TextField()
    is_virtual = models.BooleanField(default=False)
    video_url = models.CharField(verbose_name="video url", max_length=200)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-id"]
        verbose_name = "event"
        verbose_name_plural = "events"


class BatchManager(models.Manager):
    def filter_by_saler(self, *args: Any, **kwargs: Any):

        return (
            self.filter(
                Q(event=kwargs.get("event_pk"))
                & (
                    Q(sales_qtd__gte=kwargs.get("sales_qtd"))
                    | Q(batch_stop_date__gte=kwargs.get("batch_stop_date"))
                )
            )
            .order_by("-id")
            .first()
        )

    def is_valid_change(self, *args: Any, **kwargs: Any):
        event_pk = kwargs.get("event_pk")
        id = kwargs.get("id")
        sales_qtd = kwargs.get("sales_qtd")
        batch_stop_date = kwargs.get("batch_stop_date")
        batches = self.filter(event=event_pk)
        is_valid = True
        for batch in batches:
            if batch.id < id and (
                batch.sales_qtd >= sales_qtd
                or batch.batch_stop_date >= batch_stop_date
            ):
                is_valid = False
            elif batch.id > id and (
                batch.sales_qtd <= sales_qtd
                or batch.batch_stop_date <= batch_stop_date
            ):
                is_valid = False
        return is_valid


class Batch(models.Model):
    objects = BatchManager()
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    percentage = models.DecimalField(max_digits=5, decimal_places=2)
    sales_qtd = models.IntegerField()
    batch_stop_date = models.DateTimeField(verbose_name="batch stop date")
    description = models.CharField(max_length=150)
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.description

    class Meta:
        ordering = ["event_id"]
        verbose_name = "batch"
        verbose_name_plural = "batches"


class LeasingManage(models.Manager):
    def get_leasing(self, *args: Any, **kwargs: Any):
        leases = self.filter(
            Q(event=kwargs.get("event_pk")) & Q(is_active=True)
        )
        units_solid = 0
        for leasing in leases:
            units_solid += leasing.units_solid
        batch = Batch.objects.filter(
            Q(event=kwargs.get("event_pk"))
            & Q(batch_stop_date__gt=timezone.now())
            # & Q(sales_qtd__gt=units_solid)
        ).first()
        if batch is not None:
            for leasing in leases:
                leasing.sale_price = leasing.store_price * (
                    (batch.percentage / 100) + 1
                )
                leasing.student_price = (
                    leasing.store_price * ((batch.percentage / 100) + 1)
                ) / 2
        return leases


class Leasing(models.Model):
    objects = LeasingManage()
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=True)
    descroption = models.CharField(max_length=150, blank=True)
    is_active = models.BooleanField(default=True)
    store_price = models.DecimalField(
        verbose_name="store price", max_digits=8, decimal_places=2
    )
    sale_price = models.DecimalField(
        verbose_name="sale price",
        max_digits=8,
        decimal_places=2,
        blank=True,
        default="0.00",
    )
    student_price = models.DecimalField(
        verbose_name="student price",
        max_digits=8,
        decimal_places=2,
        blank=True,
        default="0.00",
    )
    units_solid = models.IntegerField(default=0)
    units = models.IntegerField()
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

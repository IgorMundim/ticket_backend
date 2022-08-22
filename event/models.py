from datetime import date
from os import truncate
from typing import Any

from customer.models import Producer, Request
from django.db import models
from django.db.models import Count, Q
from django.utils import timezone
from mptt.models import MPTTModel, TreeForeignKey


class Address(models.Model):
    cep = models.CharField(max_length=8)
    complement = models.CharField(max_length=150)
    city = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    number = models.IntegerField()
    roud = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
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
        # return "%s | " % (self.image_url)

    class Meta:
        verbose_name = "image"
        verbose_name_plural = "images"


class EventManager(models.Manager):
    def get_event(self):
        return (
            self.filter(is_published=True).order_by("-id")
            # .select_related("producer", "address")
        )


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


class Event(models.Model):
    objects = EventManager()
    producer = models.ForeignKey(Producer, on_delete=models.CASCADE)
    address = models.ForeignKey(
        Address,
        on_delete=models.PROTECT,
    )
    categories = models.ManyToManyField(Category, blank=True)
    image = models.OneToOneField(Image, on_delete=models.PROTECT)
    name = models.CharField(max_length=100)
    in_room = models.BooleanField(verbose_name="in room", default=True)
    date_end = models.DateTimeField(verbose_name="date end")
    date_start = models.DateTimeField(verbose_name="date start")
    description = models.CharField(max_length=250)
    is_virtual = models.BooleanField(default=False)
    video_url = models.CharField(verbose_name="video url", max_length=200)
    is_published = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "event"
        verbose_name_plural = "events"


class BatchManager(models.Manager):
    def filter_by_saler(self, *args: Any, **kwargs: Any):

        return (
            self.filter(
                Q(event=kwargs.get("event_pk"))
                & (
                    Q(sales_qtd__gte=kwargs.get("sales_qtd"))
                    | Q(batck_stop_date__gte=kwargs.get("batck_stop_date"))
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
        batches =  self.filter(event=event_pk)
        is_valid = True
        for batch in batches:
            if(batch.id < id and batch.sales_qtd >= sales_qtd and batch.batck_stop_date >= batch_stop_date):
                is_valid = False
            elif(batch.id > id and batch.sales_qtd <= sales_qtd and batch.batck_stop_date <= batch_stop_date):
                is_valid = False
        
        return is_valid

class Batck(models.Model):
    objects = BatchManager()
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    sequence = models.IntegerField()
    percentage = models.DecimalField(max_digits=3, decimal_places=2)
    sales_qtd = models.IntegerField()
    batck_start_date = models.DateTimeField(verbose_name="batck start date")
    batck_stop_date = models.DateTimeField(verbose_name="batck stop date")
    description = models.CharField(max_length=150)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.sequence

    class Meta:
        ordering = ["event_id"]
        verbose_name = "batch"
        verbose_name_plural = "batches"


class TicketLeasingManage(models.Manager):
    def get_leasing(self, *args: Any, **kwargs: Any):
        leases = self.filter(event=kwargs.get("event_pk")).annotate(
            solid_total=Count("units_solid")
        )

        batck = Batck.objects.filter(
            Q(event=kwargs.get("event_pk"))
            & Q(batck_stop_date__gt=timezone.now())
            & Q(batck_start_date__lte=timezone.now())
            & Q(sales_qtd__gt=leases[0].solid_total)
        ).first()

        for leasing in leases:
            leasing.sale_price = leasing.store_price * (
                (batck.percentage / 100) + 1
            )
            leasing.student_price = (
                leasing.store_price * ((batck.percentage / 100) + 1)
            ) / 2
        return leases


class TicketLeasing(models.Model):
    objects = TicketLeasingManage()
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=True)
    descroption = models.CharField(max_length=150, blank=True)
    is_active = models.BooleanField(default=True)
    store_price = models.DecimalField(
        verbose_name="store price", max_digits=6, decimal_places=2
    )
    sale_price = models.DecimalField(
        verbose_name="sale price", max_digits=6, decimal_places=2
    )
    student_price = models.DecimalField(
        verbose_name="student price", max_digits=6, decimal_places=2
    )
    units_solid = models.IntegerField()
    units = models.IntegerField()

    def __str__(self):
        return self.name


class Ticket(models.Model):
    request_id = models.ForeignKey(Request, on_delete=models.PROTECT)
    ticket_leasing_id = models.ForeignKey(
        TicketLeasing, on_delete=models.CASCADE
    )
    code = models.CharField(max_length=255)
    is_student = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.code

    class Meta:
        ordering = ["request_id"]
        verbose_name = "ticket"
        verbose_name_plural = "tickets"

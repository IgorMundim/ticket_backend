from customer.models import Address, Producer, Request, Telephone
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey


class Event(models.Model):
    producer_id = models.ForeignKey(Producer, on_delete=models.CASCADE)
    address_id = models.OneToOneField(
        Address,
        on_delete=models.PROTECT,
    )
    telephone_id = models.OneToOneField(
        Telephone,
        on_delete=models.PROTECT,
    )
    name = models.CharField(max_length=100)
    in_room = models.BooleanField(verbose_name="in room", default=True)
    date_end = models.DateTimeField(verbose_name="date end")
    date_start = models.DateTimeField(verbose_name="date start")
    description = models.CharField(max_length=250, default="")
    is_virtual = models.BooleanField(default=False)
    video_url = models.CharField(verbose_name="video url", max_length=200)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "event"
        verbose_name_plural = "events"


class Image(models.Model):
    event_id = models.ForeignKey(Event, on_delete=models.CASCADE)
    image_url = models.ImageField(
        max_length=200,
        upload_to="core/covers/%Y/%m/%d/",
        blank=True,
        default="",
    )
    alt_text = models.CharField(max_length=150)

    class Meta:
        odering = ["event_id"]

    def __str__(self):
        return self.alt_text

    class Meta:
        verbose_name = "image"
        verbose_name_plural = "images"


class Category(models.Model):
    events = models.ManyToManyField(
        Event,
    )
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True)
    # parent = TreeForeignKey(
    #     "self",
    #     on_delete=models.PROTECT,
    #     related_name="children",
    #     null=True,
    #     blank=True,
    # )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        verbose_name = "category"
        verbose_name_plural = "categories"


class Batck(models.Model):
    event_id = models.ForeignKey(Event, on_delete=models.CASCADE)
    sequence = models.IntegerField()
    batck_start_date = models.DateTimeField(verbose_name="batck start date")
    batck_stop_date = models.DateTimeField(verbose_name="batck start date")
    description = models.CharField(max_length=150, default="")
    is_active = models.BooleanField(True)

    def __str__(self):
        return self.sequence

    class Meta:
        ordering = ["event_id"]
        verbose_name = "batch"
        verbose_name_plural = "batches"


class TicketLeasing(models.Model):
    batck_id = models.ForeignKey(Batck, on_delete=models.CASCADE)
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

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["batck_id"]


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


class Stock(models.Model):
    ticket_leasing_id = models.OneToOneField(
        TicketLeasing,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    units = models.IntegerField()
    units_sold = models.IntegerField(default=0)
    last_checked = models.DateTimeField(
        verbose_name="last checked", auto_now=True
    )

    def __str__(self):
        return self.units

    class Meta:
        ordering = ["ticket_leasing_id"]
        verbose_name = "stock"
        verbose_name_plural = "stocks"

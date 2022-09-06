from django.contrib import admin

from event import models


@admin.register(models.Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("name", "date_end", "date_start", "is_published")
    search_fields = ("name",)
    list_filter = ("is_virtual", "is_published", "in_room")


@admin.register(models.Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = (
        "zipcode", "uf", "city", "neighborhood", "number",
        "street"
    )
    search_fields = ("zipcode", "uf", "city")
    list_filter = ("zipcode", "uf", "city")


@admin.register(models.Image)
class ImagemAdmin(admin.ModelAdmin):
    list_display = ("image_url", "alt_text")


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "is_active", "image_url", "alt_text")
    search_fields = ("name", "is_active")
    list_filter = ("name", "is_active")


@admin.register(models.Leasing)
class LeasingAdmin(admin.ModelAdmin):
    list_display = (
        "event", "name", "is_active",
        "store_price", "units_solid", "units",
    )
    list_filter = ("is_active",)


@admin.register(models.Batch)
class BatchAdmin(admin.ModelAdmin):
    list_display = (
        "event", "percentage", "sales_qtd", "batch_stop_date",
        "description", "is_active"
    )
    list_filter = ("is_active",)
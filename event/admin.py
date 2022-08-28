from django.contrib import admin

from event.models import (Address, Batch, Category, Event, Image, Leasing,
                          Ticket)

# Register your models here.
admin.site.register(Event)
admin.site.register(Address)
admin.site.register(Image)
admin.site.register(Category)
admin.site.register(Ticket)
admin.site.register(Leasing)
admin.site.register(Batch)

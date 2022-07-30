from django.db import models

# Create your models here.

class Stock(models.Model):
    units = models.IntegerField()
    units.sold = models.IntegerField()
    last_checked = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.units
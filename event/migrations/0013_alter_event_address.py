# Generated by Django 4.0.6 on 2022-08-09 18:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0012_event_is_published'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='address',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='event.address'),
        ),
    ]

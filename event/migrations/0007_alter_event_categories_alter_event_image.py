# Generated by Django 4.0.6 on 2022-09-05 20:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0006_alter_leasing_units_solid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='categories',
            field=models.ManyToManyField(to='event.category'),
        ),
        migrations.AlterField(
            model_name='event',
            name='image',
            field=models.OneToOneField(blank=True, on_delete=django.db.models.deletion.PROTECT, to='event.image'),
        ),
    ]

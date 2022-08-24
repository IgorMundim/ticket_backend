# Generated by Django 4.0.6 on 2022-08-24 13:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_request'),
        ('event', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='request',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='account.request'),
        ),
        migrations.DeleteModel(
            name='Request',
        ),
    ]

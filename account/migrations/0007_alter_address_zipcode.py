# Generated by Django 4.0.6 on 2022-11-10 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_alter_address_types'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='zipcode',
            field=models.CharField(max_length=10),
        ),
    ]
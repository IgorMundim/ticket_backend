# Generated by Django 4.0.6 on 2022-07-31 14:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0007_address_city'),
    ]

    operations = [
        migrations.RenameField(
            model_name='address',
            old_name='type',
            new_name='types',
        ),
    ]

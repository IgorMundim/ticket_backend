# Generated by Django 4.0.6 on 2022-07-31 13:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0002_alter_account_options_alter_address_options_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='address',
            name='account_id',
        ),
    ]

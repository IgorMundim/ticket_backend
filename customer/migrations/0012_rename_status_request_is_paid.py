# Generated by Django 4.0.6 on 2022-07-31 18:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0011_account_customer_producer_request_telephone_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='request',
            old_name='status',
            new_name='is_paid',
        ),
    ]
# Generated by Django 4.0.6 on 2022-08-18 12:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0038_delete_ticketleasing'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='batck',
            options={},
        ),
        migrations.RemoveField(
            model_name='batck',
            name='sequence',
        ),
    ]

# Generated by Django 4.0.6 on 2022-07-31 23:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0007_rename_event_category_category_events'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='parent',
        ),
    ]
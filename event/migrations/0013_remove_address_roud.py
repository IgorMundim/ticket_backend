# Generated by Django 4.0.6 on 2022-09-05 20:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0012_alter_event_categories_alter_event_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='address',
            name='roud',
        ),
    ]

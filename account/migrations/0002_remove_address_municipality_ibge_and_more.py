# Generated by Django 4.0.6 on 2022-08-25 12:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='address',
            name='municipality_IBGE',
        ),
        migrations.RemoveField(
            model_name='address',
            name='uf_ibge',
        ),
        migrations.AddField(
            model_name='address',
            name='telephone',
            field=models.CharField(default='', max_length=20),
        ),
        migrations.DeleteModel(
            name='Telephone',
        ),
    ]
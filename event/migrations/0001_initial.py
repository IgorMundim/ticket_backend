# Generated by Django 4.0.6 on 2022-08-22 18:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('customer', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cep', models.CharField(max_length=8)),
                ('complement', models.CharField(max_length=150)),
                ('city', models.CharField(max_length=100)),
                ('district', models.CharField(max_length=100)),
                ('number', models.IntegerField()),
                ('roud', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=100)),
                ('uf', models.CharField(max_length=2)),
            ],
            options={
                'verbose_name': 'address',
                'verbose_name_plural': 'adresses',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField(unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('image_url', models.ImageField(blank=True, max_length=200, upload_to='covers/%Y/%m/%d/')),
                ('alt_text', models.CharField(max_length=150)),
            ],
            options={
                'verbose_name': 'category',
                'verbose_name_plural': 'categories',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('in_room', models.BooleanField(default=True, verbose_name='in room')),
                ('date_end', models.DateTimeField(verbose_name='date end')),
                ('date_start', models.DateTimeField(verbose_name='date start')),
                ('description', models.CharField(max_length=250)),
                ('is_virtual', models.BooleanField(default=False)),
                ('video_url', models.CharField(max_length=200, verbose_name='video url')),
                ('is_published', models.BooleanField(default=True)),
                ('address', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='event.address')),
                ('categories', models.ManyToManyField(blank=True, to='event.category')),
            ],
            options={
                'verbose_name': 'event',
                'verbose_name_plural': 'events',
            },
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_url', models.ImageField(blank=True, max_length=200, upload_to='covers/%Y/%m/%d/')),
                ('alt_text', models.CharField(max_length=150)),
            ],
            options={
                'verbose_name': 'image',
                'verbose_name_plural': 'images',
            },
        ),
        migrations.CreateModel(
            name='Leasing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100)),
                ('descroption', models.CharField(blank=True, max_length=150)),
                ('is_active', models.BooleanField(default=True)),
                ('store_price', models.DecimalField(decimal_places=2, max_digits=8, verbose_name='store price')),
                ('sale_price', models.DecimalField(blank=True, decimal_places=2, max_digits=8, verbose_name='sale price')),
                ('student_price', models.DecimalField(blank=True, decimal_places=2, max_digits=8, verbose_name='student price')),
                ('units_solid', models.IntegerField()),
                ('units', models.IntegerField()),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='event.event')),
            ],
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sale_price', models.DecimalField(decimal_places=2, max_digits=8, verbose_name='sale price')),
                ('code', models.CharField(max_length=255)),
                ('is_student', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('request_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='customer.request')),
                ('ticket_leasing_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='event.leasing')),
            ],
            options={
                'verbose_name': 'ticket',
                'verbose_name_plural': 'tickets',
                'ordering': ['request_id'],
            },
        ),
        migrations.AddField(
            model_name='event',
            name='image',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='event.image'),
        ),
        migrations.AddField(
            model_name='event',
            name='producer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customer.producer'),
        ),
        migrations.CreateModel(
            name='Batck',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('percentage', models.DecimalField(decimal_places=0, max_digits=3)),
                ('sales_qtd', models.IntegerField()),
                ('batck_stop_date', models.DateTimeField(verbose_name='batck stop date')),
                ('description', models.CharField(max_length=150)),
                ('is_active', models.BooleanField(default=True)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='event.event')),
            ],
            options={
                'verbose_name': 'batch',
                'verbose_name_plural': 'batches',
                'ordering': ['event_id'],
            },
        ),
    ]
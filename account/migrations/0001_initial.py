# Generated by Django 4.0.6 on 2022-09-06 15:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(auto_now=True, verbose_name='last login')),
                ('username', models.CharField(max_length=60, unique=True)),
                ('email', models.CharField(max_length=60, unique=True)),
                ('profile_image', models.ImageField(blank=True, default='', upload_to='account/covers/%Y/%m/%d/')),
                ('hide_email', models.BooleanField(default=True)),
                ('is_superuser', models.BooleanField(default=False)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'account',
                'verbose_name_plural': 'account',
                'ordering': ['email'],
            },
        ),
        migrations.CreateModel(
            name='Producer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('business_name', models.CharField(max_length=100, verbose_name='business name')),
                ('cnpj', models.CharField(max_length=14)),
                ('fantasy_name', models.CharField(max_length=45, verbose_name='fantasy name')),
                ('state_registration', models.CharField(max_length=45, verbose_name='state registration')),
                ('municype_registration', models.CharField(max_length=45, verbose_name='municype registration')),
                ('account', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'producer',
                'verbose_name_plural': 'producers',
            },
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100, verbose_name='first name')),
                ('last_name', models.CharField(max_length=100, verbose_name='last name')),
                ('cpf', models.CharField(max_length=8)),
                ('britday', models.DateField()),
                ('account', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'customer',
                'verbose_name_plural': 'customers',
            },
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('telephone', models.CharField(default='', max_length=20)),
                ('zipcode', models.CharField(max_length=8)),
                ('complement', models.CharField(default='', max_length=150)),
                ('city', models.CharField(default='', max_length=100)),
                ('neighborhood', models.CharField(max_length=100)),
                ('number', models.IntegerField()),
                ('street', models.CharField(max_length=100)),
                ('uf', models.CharField(max_length=2)),
                ('types', models.IntegerField()),
                ('account', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'address',
                'verbose_name_plural': 'addresses',
            },
        ),
    ]

# Generated by Django 4.2.11 on 2024-03-13 10:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='EquipmentType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('abbreviation', models.CharField(max_length=10, unique=True)),
                ('slug', models.SlugField(blank=True, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Equipment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=10)),
                ('serial_number', models.CharField(max_length=20)),
                ('model_number', models.CharField(max_length=20)),
                ('brand', models.CharField(max_length=30)),
                ('price', models.FloatField()),
                ('buy_date', models.DateField()),
                ('under_repair', models.BooleanField(default=False)),
                ('functional', models.BooleanField(default=True)),
                ('slug', models.SlugField(blank=True, unique=True)),
                ('equipment_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='equipment', to='store.equipmenttype')),
            ],
        ),
        migrations.CreateModel(
            name='Allocation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('allocated_date', models.DateField(auto_now_add=True)),
                ('release_date', models.DateField(blank=True, null=True)),
                ('slug', models.SlugField(unique=True)),
                ('returned', models.BooleanField(default=False)),
                ('equipment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='allocation', to='store.equipment')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
# Generated by Django 3.1.3 on 2021-01-15 08:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('grocery_management', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ordered', models.BooleanField(default=False)),
                ('total_price', models.FloatField(default=0)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ColorVariant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('colour_name', models.CharField(max_length=30)),
                ('colour_code', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_name', models.CharField(max_length=30)),
                ('image', models.ImageField(upload_to='static/products')),
                ('price', models.CharField(max_length=15)),
                ('description', models.TextField()),
                ('quantity_available', models.IntegerField(default=10)),
                ('colour_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='grocery_management.colorvariant')),
            ],
        ),
        migrations.CreateModel(
            name='QuantityVariant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('variant_name', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='SizeVariant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size_name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='ItemImages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='static/products')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='grocery_management.item')),
            ],
        ),
        migrations.AddField(
            model_name='item',
            name='quantity_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='grocery_management.quantityvariant'),
        ),
        migrations.AddField(
            model_name='item',
            name='size_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='grocery_management.sizevariant'),
        ),
        migrations.CreateModel(
            name='CartItems',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.FloatField(default=0)),
                ('quantity', models.IntegerField(default=1)),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='grocery_management.cart')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='grocery_management.item')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

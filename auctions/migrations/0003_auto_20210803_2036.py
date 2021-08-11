# Generated by Django 3.2.5 on 2021-08-03 19:36

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_alter_listing_image_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='category',
            field=models.CharField(blank=True, choices=[('Beauty', 'Beauty'), ('Books', 'Books'), ('CDs', 'Cds'), ('Clothing', 'Clothing'), ('Computers', 'Computers'), ('Home & Kitchen', 'Home And Kitchen'), ('Shoes & Bags', 'Shoes And Bags'), ('Toys & Games', 'Toys And Games')], max_length=14, null=True),
        ),
        migrations.AlterField(
            model_name='listing',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(1)]),
        ),
    ]
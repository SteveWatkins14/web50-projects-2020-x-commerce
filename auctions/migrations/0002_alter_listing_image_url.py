# Generated by Django 3.2.5 on 2021-08-02 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='image_url',
            field=models.URLField(blank=True),
        ),
    ]

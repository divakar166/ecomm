# Generated by Django 4.2.4 on 2023-08-24 14:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_remove_cartitems_color_variant_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitems',
            name='quantity',
            field=models.IntegerField(default=1),
        ),
    ]
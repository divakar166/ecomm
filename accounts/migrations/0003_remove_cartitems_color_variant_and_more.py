# Generated by Django 4.2.4 on 2023-08-24 13:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_cart_cartitems'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartitems',
            name='color_variant',
        ),
        migrations.RemoveField(
            model_name='cartitems',
            name='size_variant',
        ),
    ]

# Generated by Django 3.1 on 2020-08-26 04:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0003_cartitem_item_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartitem',
            name='item_price',
        ),
        migrations.RemoveField(
            model_name='cartitem',
            name='payment',
        ),
    ]
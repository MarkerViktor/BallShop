# Generated by Django 3.1.5 on 2021-01-30 06:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0003_auto_20210130_1231'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shoppingcart',
            name='specific_products',
        ),
        migrations.AddField(
            model_name='shoppingcart',
            name='products',
            field=models.ManyToManyField(to='order.ProductInCart', verbose_name='List of selected products'),
        ),
    ]

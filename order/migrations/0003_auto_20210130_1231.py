# Generated by Django 3.1.5 on 2021-01-30 06:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_auto_20210130_1230'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='creation_time',
            field=models.DateTimeField(),
        ),
    ]

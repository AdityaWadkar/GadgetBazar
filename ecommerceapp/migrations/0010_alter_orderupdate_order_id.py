# Generated by Django 3.2.20 on 2023-09-03 08:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerceapp', '0009_auto_20230902_2353'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderupdate',
            name='order_id',
            field=models.CharField(default='', max_length=100),
        ),
    ]

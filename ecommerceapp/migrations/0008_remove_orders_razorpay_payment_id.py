# Generated by Django 3.2.20 on 2023-09-02 11:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerceapp', '0007_orders_razorpay_payment_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orders',
            name='razorpay_payment_id',
        ),
    ]

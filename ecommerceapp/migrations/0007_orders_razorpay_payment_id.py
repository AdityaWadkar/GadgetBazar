# Generated by Django 3.2.20 on 2023-09-02 11:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerceapp', '0006_auto_20230902_1050'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='razorpay_payment_id',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
